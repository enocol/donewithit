from django.shortcuts import render
from products.models import Product

# Create your views here.
def home(request):
    '''Home page view'''
    featured_products = Product.objects.filter(is_featured=True)
    return render(request, 'home/home.html', {'featured_products': featured_products})
