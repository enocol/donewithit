from django.shortcuts import render
from products.models import Product
from .forms import ProductEditForm, MoreProductImageFormSet

from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def profile(request):

    """
    Render the user profile page.
    """
    products = Product.objects.filter(seller=request.user)  
   
    context = {
        'products': products,
        
    }
    return render(request, 'profiles/profile.html', context)


@login_required
@transaction.atomic
def product_edit(request, product_id):
    product = get_object_or_404(Product, pk=product_id)


    if request.method == "POST":
        form = ProductEditForm(request.POST, request.FILES, instance=product)
        formset = MoreProductImageFormSet(request.POST, request.FILES, instance=product, prefix="images")

        form_ok = form.is_valid()
        formset_ok = formset.is_valid()

        if form_ok and formset_ok:
            form.save()
            formset.save()
            messages.success(request, "Product updated successfully.")
            return redirect(reverse("product_detail", args=[product.pk]))

       
        if not form_ok:
            print("FORM ERRORS:", form.errors.as_json())
            messages.error(request, f"Product form error(s): {form.errors.as_text()}")
        if not formset_ok:
            print("FORMSET NON-FORM ERRORS:", formset.non_form_errors())
            for i, f in enumerate(formset.forms):
                if f.errors:
                    print(f"FORMSET[{i}] ERRORS:", f.errors.as_json())
            messages.error(request, "Please fix the errors below.")

    else:
        form = ProductEditForm(instance=product)
        formset = MoreProductImageFormSet(instance=product, prefix="images")

    return render(request, "profiles/edit_product.html", {
       "form": form,
       "formset": formset,
       "product": product,
   })
@login_required
def product_delete(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect('product_list')  

    return render(request, 'profiles/confirm_delete.html', {'product': product})

