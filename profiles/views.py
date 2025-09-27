from django.shortcuts import render
from products.management.commands.populate_data import User
from products.models import Product
from .forms import ProductEditForm, MoreProductImageFormSet, ProfileForm, UserForm
from .models import Profile
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile
from .forms import UserForm, ProfileForm


# Create your views here.

@login_required
def profile(request):

    """
    Render the user profile page.
    """
    products = Product.objects.filter(seller=request.user)
    profile, _ = Profile.objects.get_or_create(user=request.user)
    
   
    context = {
        'products': products,
        'profile': profile,
        
    }
    return render(request, 'profiles/profile.html', context)



@login_required
def edit_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        uform = UserForm(request.POST, instance=request.user)
        pform = ProfileForm(request.POST, request.FILES, instance=profile)
        if uform.is_valid() and pform.is_valid():
            uform.save()
            pform.save()
            messages.success(request, "Your profile has been updated.")
            return redirect("profile") 
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        uform = UserForm(instance=request.user)
        pform = ProfileForm(instance=profile)

        context = {
            "uform": uform,
            "pform": pform,
            
        }

    return render(request, "profiles/edit_profile.html", context)

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

