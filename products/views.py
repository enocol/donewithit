from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Product
from .models import Category
from .forms import MoreProductImageFormSet, ProductForm
from django.contrib.auth.decorators import login_required

def product_list(request):
    categories = Category.objects.all()  # Assuming you want to use categories in the template
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', None)
    

    if search_query:
        products = Product.objects.filter(
            Q(product_name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
        if not products.exists():
            messages.error(request, "No products found matching your search criteria.")
            products = Product.objects.all()  # Return all products if no products found
    else:
        products = Product.objects.all()  # or .none() if you want no default results
       

    if category_filter:
        products = products.filter(category__name=category_filter)
    else:
        products = Product.objects.all()

    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.images.exists():
        images = product.images.all()
    categories = Category.objects.all()  # Fetch all categories for the template
    if not product:
        messages.error(request, "Product not found.")
        return render(request, 'products/product_list.html', {})

    context = {
        'product': product,
        'categories': categories,
        'images': images if 'images' in locals() else None,  # Check if images exist
    }
    return render(request, 'products/product_detail.html', context)

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        formset = MoreProductImageFormSet(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user  # Assuming you want to associate the product with the logged-in user
            formset = MoreProductImageFormSet(request.POST, request.FILES, instance=product)
            if formset.is_valid():
                product.save()
                formset.save()
                messages.success(request, "Product created successfully.")
                return redirect('product_list')  # Redirect to the product list after creation
    else:
        form = ProductForm()
        formset = MoreProductImageFormSet()

    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'products/product_form.html', context)   



