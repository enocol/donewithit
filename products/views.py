from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q

from donewithit import settings
from .models import Product
from .models import Category
from .forms import MoreProductImageFormSet, ProductForm
from django.contrib.auth.decorators import login_required

def product_list(request):
    '''Product listing view'''
    categories = Category.objects.all()  
    search_query = request.GET.get('search', None)
    category_filter = request.GET.get('category', None)
    filter_type = request.GET.get("filter")
    category_label = dict(Category.CATEGORY_TYPES).get(category_filter, 'Unknown')
    products = Product.objects.all()
    sort_option = request.GET.get('sort', '')

    if filter_type == "new_arrivals":
        ten_days_ago = timezone.now() - timedelta(days=10)
        products = Product.objects.filter(created_at__gte=ten_days_ago).order_by("-created_at")
       
        if not products.exists():
            messages.info(request, "No new arrivals in the last 10 days.")
            products = Product.objects.all()


    if sort_option == "price_asc":
        products = products.order_by("price")
    elif sort_option == "price_desc":
        products = products.order_by("-price")
    elif sort_option == "name_asc":
        products = products.order_by("product_name")
    elif sort_option == "name_desc":
        products = products.order_by("-product_name")
    elif sort_option == "date_asc":
        products = products.order_by("created_at")
    elif sort_option == "date_desc":
        products = products.order_by("-created_at")
    else:
        if sort_option == "":
            products = products.order_by("product_name")

    sort_options = [
        ("price_asc", "Price: Low to High"),
        ("price_desc", "Price: High to Low"),
        ("name_asc", "Name: A to Z"),
        ("name_desc", "Name: Z to A"),
        ("date_asc", "Date: Oldest First"),
        ("date_desc", "Date: Newest First"),
    ]
    

    if search_query:
        products = Product.objects.filter(
            Q(product_name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
        if not products.exists():
            messages.error(request, f"No products found matching '{search_query}'.")
            products = Product.objects.all()
   

    if category_filter:
        products = products.filter(category__name=category_filter)
        if not products.exists():
            messages.error(request, f"No products found in category '{category_filter}'.")
            products = Product.objects.all()
    

    context = {
        'products': products,
        'categories': categories,
        'sort_options': sort_options,
        'current_sort': sort_option,
        'search_query': search_query,
        'category_filter': category_label,
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, product_id):
    '''Product detail view'''
    product = get_object_or_404(Product, id=product_id)
    similar_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
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
        'similar_products': similar_products,
       
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
                # Send a confirmation email to the seller
                send_mail(
                    'Your product has been listed',
                    f'Thank you for listing your product {product.product_name} on our marketplace.',
                    settings.DEFAULT_FROM_EMAIL,
                    [request.user.email],
                    fail_silently=False,
                )
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



