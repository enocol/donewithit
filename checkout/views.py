from email.mime import message
from pyexpat.errors import messages
from django.shortcuts import redirect, render
from checkout.forms import CheckoutForm
from django.conf import settings
from checkout.models import Order, OrderItem
from shoppingCart.context import cart_context
from products.models import Product

import stripe

def checkout(request):
    # Placeholder for checkout logic
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_client_secret = settings.STRIPE_CLIENT_SECRET
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('product_list')
    current_cart = cart_context(request)
    total = current_cart.get('cart_total', 0)
    stripe_total = int(total * 100)  # Convert to cents for Stripe
    stripe.api_key = stripe_client_secret
    # Create a payment intent
    try:
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency='usd',
            metadata={'integration_check': 'accept_a_payment'},
        )
        # Get the client secret for the payment intent
        stripe_client_secret = intent['client_secret']
    except Exception as e:
        return render(request, 'checkout/checkout_error.html', {'error': str(e)})
    
    

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        cart = request.session.get('cart', {})
        if form.is_valid():
            form.save()
            for product_id in cart:
                product = Product.objects.get(id=product_id)
                product_name = product.name
                price = product.price
                order_item = OrderItem(
                    order=form.instance,
                    product_name=product_name,
                    price=price
                )
                if order_item.is_valid():
                    order_item.save()
            # Clear the cart after successful checkout
            request.session['cart'] = {}
            # Redirect to a success page
            return redirect('checkout_success')
    context = {
        'form': CheckoutForm(),
        'stripe_public_key': stripe_public_key,
        'stripe_client_secret': stripe_client_secret,
        'cart': cart,
    }
    return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_id):
    # Placeholder for checkout success logic
    if not request.session.get('cart'):
        return redirect('product_list')
    order = Order.objects.get(id=order_id) if order_id else None
    messages.success(request, f"Thank you for your order! Your order with number {order.id} has been successfully placed. An email confirmation will be sent to you shortly")
    context = {
        'order': order,
    }
    return render(request, 'checkout/checkout_success.html', context)