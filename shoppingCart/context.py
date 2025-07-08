

from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def cart_context(request):
    """
    Context processor to add cart information to the context.
    """
    cart = request.session.get('cart', {})
    cart_items = []

    for product_id in cart:
        cart_items.append({
            'product_name': cart[product_id]['name'],
            'price': cart[product_id]['price'],
        })

    context = {
        'cart_items': cart_items,
        'cart_total': sum(float(item['price']) for item in cart_items),
        'cart_count': len(cart_items), 
    }

    return context