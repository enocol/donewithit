
from django.urls import path
from . import views


urlpatterns = [
    path('shopping-cart/', views.shopping_cart, name='shopping_cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]
