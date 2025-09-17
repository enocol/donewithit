from django.shortcuts import render
from products.models import Category, Product

# Create your views here.
def home(request):
    '''Home page view'''
    featured_products = Product.objects.filter(is_featured=True)[:5]  # Get up to 5 featured products
    categories = Category.objects.all() 
    return render(request, 'home/home.html', {'featured_products': featured_products, 'categories': categories})
