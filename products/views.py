from django.shortcuts import render
from .models import Product  # Assuming Products is the model for products

# Create your views here.
def product_list(request):
    """
    View to list all products.
    """

    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'products/product_list.html', context)
