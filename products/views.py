from django.shortcuts import render
from products.models.Models_Product import Product


def list_all_products(request):
    """ This function list all products,
        including sorting and search queries """

    products = Product.objects.all()

    context = {
        'products': products
    }
    
    return render(request, 'products/products.html', context=context)
