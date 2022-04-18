from django.url import path
from . import views


urlpatterns = [
    path('', views.view_cart, name="view_cart"),
]
