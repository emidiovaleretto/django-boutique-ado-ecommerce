from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from products.models import Product


def view_cart(request):
    """ This function renders the cart content. """
    return render(request, 'cart/cart.html')


def add_to_cart(request, item_id):
    """ This function add a quantity of an specific product
        to the shopping cart. """

    product = get_object_or_404(Product, pk=item_id)
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
                messages.success(
                    request, f'Updated size {size.upper()} | {product.name} quantity to {bag[item_id]["items_by_size"][size]}.')
            else:
                cart[item_id]['items_by_size'][size] = quantity
                messages.success(
                    request, f'Added size {size.upper()} | {product.name} to your bag.')
        else:
            cart[item_id] = {'items_by_size': {size: quantity}}
            messages.success(
                request, f'Added size {size.upper()} | {product.name} to your bag.')
    else:
        if item_id in list(cart.keys()):
            cart[item_id] += quantity
            messages.success(
                request, f'Updated {product.name} quantity to {bag[item_id]}.')
        else:
            cart[item_id] = quantity
            messages.success(request, f'Added {product.name} to your bag.')

    request.session['cart'] = cart
    return redirect(redirect_url)


def adjust_quantity_to_cart(request, item_id):
    """ This function adjust the quantity of an specific product
        to the specific amount. """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = None

    if 'product_size' in request.POST:
        size = request.POST['product_size']

    cart = request.session.get('cart', {})

    if size:
        if quantity > 0:
            cart[item_id]['items_by_size'][size] = quantity
            messages.success(
                request, f'Updated size {size.upper()} | {product.name} quantity to {cart[item_id]["items_by_size"][size]}.')
        else:
            del cart[item_id]['items_by_size'][size]
            if not cart[item_id]['items_by_size']:
                cart.pop(item_id)
            messages.success(
                request, f'Removed size {size.upper()} | {product.name} from your bag.')

    else:
        if quantity > 0:
            cart[item_id] = quantity
            messages.success(
                request, f'Updated {product.name} quantity to {bag[item_id]}.')
        else:
            cart.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag.')

    request.session['cart'] = cart
    return redirect(reverse('view_cart'))


def remove_item_from_cart(request, item_id):
    """ This function removes the item from the shopping cart. """

    try:
        product = get_object_or_404(Product, pk=item_id)
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']

        cart = request.session.get('cart', {})

        if size:
            del cart[item_id]['items_by_size'][size]
            if not cart[item_id]['items_by_size']:
                cart.pop(item_id)
            messages.success(
                request, f'Removed size {size.upper()} | {product.name} from your bag.')

        else:
            cart.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag.')

        request.session['cart'] = cart
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
