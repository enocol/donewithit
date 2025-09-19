from django.contrib import admin

# Register your models here.
from .models import Subscriber
@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_confirmed', 'created_at')
    search_fields = ('email',)
    list_filter = ('is_confirmed', 'created_at')
    readonly_fields = ('confirm_token', 'unsubscribe_token', 'created_at')

    fieldsets = (
        (None, {
            'fields': ('email', 'is_confirmed', 'created_at', 'confirm_token', 'unsubscribe_token')
        }),
    )
