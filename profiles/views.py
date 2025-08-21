from django.shortcuts import render
import products
from products.models import Product
from .forms import ProductEditForm, MoreProductImageFormSet

from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib import messages
from django.db import transaction


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



@transaction.atomic
def product_edit(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == "POST":
        form = ProductEditForm(request.POST, request.FILES, instance=product)
        formset = MoreProductImageFormSet(request.POST, request.FILES, instance=product, prefix="images")
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Product updated successfully.")
            return redirect(reverse("product_detail", args=[product.pk]))
        messages.error(request, "Please fix the errors below.")
    else:
        form = ProductEditForm(instance=product)
        formset = MoreProductImageFormSet(instance=product, prefix="images")

    return render(request, "profiles/edit_product.html", {
        "form": form,
        "formset": formset,
        "product": product,
    })

