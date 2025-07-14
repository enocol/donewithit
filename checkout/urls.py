from django.contrib import admin
from django.urls import include, path

from checkout import views  

urlpatterns = [
   path('checkout/', views.checkout, name='checkout'),  # Checkout view
   path('checkout/success/<int:order_id>/', views.checkout_success, name='checkout_success'),  # Checkout success view

]