import os
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings
from .forms import OrderForm

from cart.contexts import cart_contents

import stripe

if os.path.exists('env.py'):
    import env


def checkout(request):

    stripe_public_key = os.environ.get("STRIPE_PUBLIC_KEY")
    stripe_secret_key = os.environ.get("STRIPE_SECRET_KEY")

    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "There's nothing in your bag at the moment.")
        return redirect(reverse('products'))

    current_bag = cart_contents(request)
    total = current_bag['grand_total']

    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key

    payment_intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY
    )

    order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(
            request,
            'Stripe public key is missing. '
            'Did you forget to set it in your environment?'
        )

    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': payment_intent.client_secret,
    }

    return render(request, 'checkout/checkout.html', context=context)
