from django.shortcuts import render
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

        form_ok = form.is_valid()
        formset_ok = formset.is_valid()

        if form_ok and formset_ok:
            form.save()
            formset.save()
            messages.success(request, "Product updated successfully.")
            return redirect(reverse("product_detail", args=[product.pk]))

        # Only run these on POST (so no UnboundLocalError on GET)
        # Helpful diagnostics while you debug:
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
        # GET request — just render blank/filled forms. Do NOT touch form_ok/formset_ok here.
        form = ProductEditForm(instance=product)
        formset = MoreProductImageFormSet(instance=product, prefix="images")

    return render(request, "profiles/edit_product.html", {
       "form": form,
       "formset": formset,
       "product": product,
   })

