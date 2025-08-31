from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('products', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add_product/', views.product_create, name='product_create')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
