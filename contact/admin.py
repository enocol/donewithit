from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("created_at", "name", "email", "user")
    list_filter = ("created_at",)
    search_fields = ("name", "email", "message")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
