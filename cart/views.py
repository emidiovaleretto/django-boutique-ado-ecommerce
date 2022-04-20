from django.shortcuts import render, redirect, reverse


def view_cart(request):
    """ This function renders the cart content. """
    return render(request, 'cart/cart.html')


def add_to_cart(request, item_id):
    """ This function add a quantity of an specific product
        to the shopping cart. """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None

    if 'product_size' in request.POST:
        size = request.POST['product_size']

    cart = request.session.get('cart', {})

    if size:
        if item_id in list(cart.keys()):
            if size in cart[item_id]['items_by_size'].keys():
                cart[item_id]['items_by_size'][size] += quantity
            else:
                cart[item_id]['items_by_size'][size] = quantity
        else:
            cart[item_id] = {
                'items_by_size': {size: quantity}
            }
    else:
        if item_id in list(cart.keys()):
            cart[item_id] += quantity
        else:
            cart[item_id] = quantity

    request.session['cart'] = cart
    return redirect(redirect_url)


def remove_item_from_cart(request, item_id):
    """ This function removes the item from the shopping cart. """

    quantity = int(request.POST.get('quantity'))
    size = None

    if 'product_size' in request.POST:
        size = request.POST['product_size']

    cart = request.session.get('cart', {})

    if size:
        if quantity > 0:
            cart[item_id]['items_by_size'][size] = quantity
        else:
            del cart[item_id]['items_by_size'][size]

    else:
        if quantity > 0:
            cart[item_id] = quantity
        else:
            cart.pop[item_id]

    request.session['cart'] = cart
    return redirect(reverse('view_cart'))

def adjust_quantity_to_cart(request, item_id):
    """ This function adjust the quantity of an specific product
        to the specific amount. """

    quantity = int(request.POST.get('quantity'))
    size = None

    if 'product_size' in request.POST:
        size = request.POST['product_size']

    cart = request.session.get('cart', {})

    if size:
        if quantity > 0:
            cart[item_id]['items_by_size'][size] = quantity
        else:
            del cart[item_id]['items_by_size'][size]

    else:
        if quantity > 0:
            cart[item_id] = quantity
        else:
            cart.pop[item_id]

    request.session['cart'] = cart
    return redirect(reverse('view_cart'))
