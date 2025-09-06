from django.urls import path
from . import views


urlpatterns = [
    path('profiles/', views.profile, name='profile'),
    path('profiles/edit_product/<int:product_id>/', views.product_edit, name='product_edit'),
    path('profiles/delete_product/<int:product_id>/', views.product_delete, name='product_delete'),
    path('profiles/edit_profile/', views.edit_profile, name='edit_profile'),
] 
