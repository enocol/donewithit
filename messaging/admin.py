from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Thread, Message

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "seller", "buyer", "last_message_at", "created_at")
    list_filter = ("product",)
    search_fields = ("product__product_name", "seller__username", "buyer__username")

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "thread", "sender", "recipient", "is_read", "created_at")
    list_filter = ("is_read",)
    search_fields = ("body", "sender__username", "recipient__username")

