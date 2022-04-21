import os
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm

if os.path.exists('env.py'):
    import env


def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "There's nothing in your bag at the moment.")
        return redirect(reverse('products'))

    order_form = OrderForm()
    context = {
        'order_form': order_form,
        'stripe_public_key': os.environ.get("STRIPE_PUBLIC_KEY"),
        'stripe_client_secret_key': os.environ.get("STRIPE_CLIENT_SECRET_KEY"),
    }

    return render(request, 'checkout/checkout.html', context=context)
