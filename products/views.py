from django.shortcuts import render
from django.db.models import Q
from .models import Product
from .models import Category

def product_list(request):
    categories = Category.objects.all()  # Assuming you want to use categories in the template
    search_query = request.GET.get('search', '')

    if search_query:
        products = Product.objects.filter(
            Q(product_name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    else:
        products = Product.objects.all()  # or .none() if you want no default results

    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'products/product_list.html', context)

