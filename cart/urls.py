from django.urls import path
from . import views


urlpatterns = [
    path('', views.view_cart, name="view_cart"),
    path('add/<item_id>', views.add_to_cart, name='add_to_cart'),
    path('adjust/<item_id>', views.adjust_quantity_to_cart, name='adjust_quantity_to_cart'),
    path('remove/<item_id>', views.remove_item_from_cart, name='remove_item_from_cart'),
]
