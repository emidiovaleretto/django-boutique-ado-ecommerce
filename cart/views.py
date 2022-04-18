from django.shortcuts import render


def view_cart(request):
    """ This function renders the cart content. """
    return render(request, 'cart/cart.html')
