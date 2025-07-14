from django.contrib import admin
from django.urls import include, path

from checkout import views  

urlpatterns = [
   path('checkout/', views.checkout, name='checkout'),  # Checkout view
]