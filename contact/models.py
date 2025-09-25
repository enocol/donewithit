from django.db import models
from django.conf import settings
from django.db import models

class ContactMessage(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="contact_messages",
    )
    name = models.CharField(max_length=150)  
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        sender = self.user.get_username() if self.user else self.name
        return f"Message from {sender} <{self.email}>"

