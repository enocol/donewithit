from django.db import models

# Create your models here.
import uuid
from django.db import models

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    is_confirmed = models.BooleanField(default=False)
    confirm_token = models.CharField(max_length=64, unique=True, blank=True)
    unsubscribe_token = models.CharField(max_length=64, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.confirm_token:
            self.confirm_token = uuid.uuid4().hex
        if not self.unsubscribe_token:
            self.unsubscribe_token = uuid.uuid4().hex
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.email} ({'confirmed' if self.is_confirmed else 'pending'})"
