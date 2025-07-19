from django.shortcuts import render
from products.models import Product

# Create your views here.

def profile(request):

    """
    Render the user profile page.
    """
    products = Product.objects.filter(seller=request.user)  # Assuming you want to show products created by the user
    context = {
        'products': products,
    }
    return render(request, 'profiles/profile.html', context)
