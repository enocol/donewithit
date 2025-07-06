from django.contrib import admin
from django.contrib import admin
from .models import Product, MoreProductImage, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

class MoreProductImageInline(admin.TabularInline):
    model = MoreProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [MoreProductImageInline]
    list_display = ('product_name', 'seller', 'price', 'created_at', 'updated_at')
    search_fields = ('product_name', 'description', 'seller__username')
    list_filter = ('category', 'created_at', 'updated_at')
    ordering = ('-created_at',)

admin.site.site_header = "MarketCorner Admin"
admin.site.site_title = "MarketCorner Admin Portal"