from django.shortcuts import redirect, render
from checkout.forms import CheckoutForm
from django.conf import settings

def checkout(request):
    # Placeholder for checkout logic
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_client_secret = settings.STRIPE_CLIENT_SECRET
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('product_list')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Process the form data
            # Here you would typically save the order and redirect to a success page
            return render(request, 'checkout/success.html', {'form': form})
    context = {
        'form': CheckoutForm(),
        'stripe_public_key': stripe_public_key,
        'stripe_client_secret': stripe_client_secret,
        'cart': cart,
    }
    return render(request, 'checkout/checkout.html', context)


