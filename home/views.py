from django.shortcuts import render
from products.models import Category, Product
from subscriptions.forms import NewsletterSignupForm

# Create your views here.
def home(request):
    '''Home page view'''
    featured_products = Product.objects.filter(is_featured=True) 
    categories = Category.objects.all() 
    

    content = {
        'featured_products': featured_products,
        'categories': categories,
       
    }
    return render(request, 'home/home.html', content)
