from django.contrib import admin

from checkout.models import Order, OrderItem

# Register your models here.
class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('orderitem_total',)

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemAdmin]
    readonly_fields = ('order_number', 'created_at', 'order_total', 'grand_total')
    fields = ('first_name', 'last_name', 'email', 'address', 'city', 'state', 'post_code', 'country', 'order_total', 'grand_total')
    list_display = ('order_number', 'first_name', 'last_name', 'email', 'created_at', 'order_total', 'grand_total')

    ordering = ('-created_at',)

admin.site.register(Order, OrderAdmin)
