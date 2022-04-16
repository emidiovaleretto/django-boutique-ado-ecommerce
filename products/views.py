from django.shortcuts import render, get_object_or_404
from products.models.Models_Product import Product


def list_all_products(request):
    """ This function list all products,
        including sorting and search queries """

    products = Product.objects.all()

    context = {
        'products': products
    }
    
    return render(request, 'products/products.html', context=context)


def product_detail(request, product_id):
    """ This function returns an individual product by its id """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product
    }

    return render(request, 'products/product_detail.html', context=context)