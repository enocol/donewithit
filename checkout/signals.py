from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from checkout.models import OrderItem

@receiver(post_save, sender=OrderItem)
def update_order_total(sender, instance, **kwargs):
    instance.order.calculate_order_total()

@receiver(post_delete, sender=OrderItem)
def update_order_total_on_delete(sender, instance, **kwargs):
    instance.order.calculate_order_total()