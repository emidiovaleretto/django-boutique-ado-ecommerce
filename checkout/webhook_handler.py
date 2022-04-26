from django.http import HttpResponse
from .models import Order, OrderLineItem
from products.models import Product

from time import sleep

import json


class StripeWHookHandler:
    """
    Class to handle Stripe Webhooks
    """

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        This method handles a generic/unknown/
        unexpected webhook event.
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """
        This method handles the payment_intent.succeeded
        webhook event from Stripe.
        """

        payment_intent = event.data.object
        payment_id = payment_intent.id
        cart = payment_intent.metadata.cart
        save_info = payment_intent.metadata.save_info

        billing_details = payment_intent.charges.data[0].billing_details
        shipping_details = payment_intent.shipping

        grand_total = round(payment_intent.charges.data[0].amount / 100, 2)

        for field, value in shipping_details.address.items():
            if value == '':
                shipping_details.address[field] = None

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    street_address_1__iexact=shipping_details.address.line1,
                    street_address_2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    grand_total=grand_total,
                    original_cart=cart,
                    stripe_payment_id=payment_id
                )

                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                sleep(1)

        if order_exists:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} '
                '| Success: verified order already in database',
                status=200
            )
        else:
            order = None
            try:
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    town_or_city=shipping_details.address.city,
                    street_address_1=shipping_details.address.line1,
                    street_address_2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    original_cart=cart,
                    stripe_payment_id=payment_id
                )
                for item_id, item_data in json.load(cart).items():
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data
                        )
                        order_line_item.save()
                    else:
                        for (size,
                             quantity) in item_data['items_by_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size
                            )
                            order_line_item.save()

            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | Error: {e}',
                    status=500
                )
        return HttpResponse(
            content=f'Webhook received: {event["type"]} '
                     '| Success: order created in webhook',
            status=200
        )

    def handle_payment_intent_payment_failed(self, event):
        """
        This method handles the payment_intent.payment_failed
        webhook event from Stripe.
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )
