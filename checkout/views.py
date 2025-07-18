from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
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
        if form.is_valid():
            order = form.save()

            for product_id in cart:
                product = get_object_or_404(Product, id=product_id)
                order_item = OrderItem(
                        order=order,
                        product=product,
                        price=product.price
                    )
                order_item.save()


            
            return redirect('checkout_success', order_id=order.id)
    else:
        form = CheckoutForm()
    

    
    context = {
        'form': CheckoutForm(),
        'stripe_public_key': stripe_public_key,
        'stripe_client_secret': stripe_client_secret,
        'cart': cart,
    }
    return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_id=None):
    # Placeholder for checkout success logic
   
    order = Order.objects.get(id=order_id) if order_id else None
    messages.success(request, f'Your order has been placed successfully!, you order id is {order.id}')
    if not order:
        return redirect('product_list')
    
    order.calculate_order_total()
    request.session['cart'] = {}

    
    context = {
        'order': order,
    }
    return render(request, 'checkout/checkout_success.html', context)