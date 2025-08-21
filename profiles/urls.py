from django.urls import path
from . import views


urlpatterns = [
    path('profiles/', views.profile, name='profile'),
    path('profiles/edit_product/<int:product_id>/', views.product_edit, name='product_edit'),
] 
