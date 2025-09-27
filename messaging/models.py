from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models
from django.utils import timezone
from products.models import Product

User = settings.AUTH_USER_MODEL

class Thread(models.Model):
    """A private conversation between a buyer and the seller about a product."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="threads")
    seller  = models.ForeignKey(User, on_delete=models.CASCADE, related_name="threads_as_seller")
    buyer   = models.ForeignKey(User, on_delete=models.CASCADE, related_name="threads_as_buyer")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_message_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("product", "seller", "buyer")
        ordering = ("-last_message_at", "-updated_at")

    def __str__(self):
        return f"Thread #{self.pk} • {self.product} • {self.buyer} ↔ {self.seller}"

    def other_user(self, user):
        return self.seller if user == self.buyer else self.buyer

class Message(models.Model):
    """A single message inside a Thread."""
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return f"Msg #{self.pk} in Thread #{self.thread_id} from {self.sender}"

    def save(self, *args, **kwargs):
        new = self.pk is None
        super().save(*args, **kwargs)
        if new:
            # bump thread activity
            Thread.objects.filter(pk=self.thread_id).update(last_message_at=timezone.now())

