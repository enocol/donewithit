from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from products.models import Product

# Create your views here.


def shopping_cart(request):
    """
    View function to render the shopping cart page.
    """
    
    return render(request, 'shoppingCart/shopping_cart.html')



@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    if request.method == 'POST':
        # Check if product is already in cart
        if str(product_id) in cart:
            messages.info(request, f"{product.product_name} is already in your cart.")
        else:
            # Add new product to cart
            cart[str(product_id)] = {
                'name': product.product_name,
                'price': str(product.price), 
            }
            messages.success(request, f"{product.product_name} has been successfully added to your cart.")
        
        # Save cart back to session
        request.session['cart'] = cart

        return redirect('product_detail', product_id=product.id)

    
    return render(request, 'products/product_detail.html', {'product': product})

@login_required
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
        messages.success(request, "Item has been removed from your cart.")
    else:
        messages.error(request, "Item not found in your cart.")

    return redirect('shopping_cart')
