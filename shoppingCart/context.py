

from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def cart_context(request):
    """
    Context processor to add cart information to the context.
    """
    delivery_charge = settings.DELIVERY_CHARGE
    cart = request.session.get('cart', {})
    cart_items = []

    for product_id in cart:
        product = get_object_or_404(Product, id=product_id)
        cart_items.append({
            "product_id": product.id, 
            'product_name': cart[product_id]['name'],
            'price': cart[product_id]['price'],
            'main_image': product.main_image.url if product.main_image else None,
        })

    context = {
        'cart_items': cart_items,
        'cart_total': sum(float(item['price']) for item in cart_items),
        'cart_count': len(cart_items), 
        'delivery_charge': delivery_charge,
    }

    return context