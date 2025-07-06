from django.shortcuts import render

# Create your views here.
def product_list(request):
    """
    View to list all products.
    """
    # Here you would typically fetch products from the database
    # For now, we will just render an empty template
    return render(request, 'products/product_list.html', {})
