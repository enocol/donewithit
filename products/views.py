from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Product
from .models import Category
from .forms import MoreProductImageFormSet, ProductForm
from django.contrib.auth.decorators import login_required

def product_list(request):
    '''Product listing view'''
    categories = Category.objects.all()  
    search_query = request.GET.get('search', None)
    category_filter = request.GET.get('category', None)
    products = Product.objects.all()
    

    if search_query:
        products = Product.objects.filter(
            Q(product_name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    if not products.exists():
        messages.error(request, "No products found matching your search criteria.")
        products = Product.objects.all()

    if category_filter:
        products = products.filter(category__name=category_filter)

    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, product_id):
    '''Product detail view'''
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()  

    if product.images.exists():
        images = product.images.all()
    
    if not product:
        messages.error(request, "Product not found.")
        return render(request, 'products/product_list.html', {})

    context = {
        'product': product,
        'categories': categories,
        'images': images if 'images' in locals() else None, 
    }
    return render(request, 'products/product_detail.html', context)

@login_required
def product_create(request):
    '''Product creation view'''
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        formset = MoreProductImageFormSet(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user  
            formset = MoreProductImageFormSet(request.POST, request.FILES, instance=product)
            if formset.is_valid():
                product.save()
                formset.save()
                messages.success(request, "Product created successfully.")
                return redirect('product_list')
    else:
        form = ProductForm()
        formset = MoreProductImageFormSet()

    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'products/product_form.html', context)   



