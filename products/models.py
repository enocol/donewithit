from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.

from django.db import models

class Category(models.Model):
    CATEGORY_TYPES = [
        
        ('BOOKS', 'Books'),
        ('CLOTHING', 'Clothing'),
        ('ELECTRONICS', 'Electronics'),
        ('FURNITURE', 'Furniture'),
        ('TOYS', 'Toys'),
        ('SPORTS', 'Sports Equipment'),
        ('MISCELLANEOUS', 'Miscellaneous'),
        ('OTHER', 'Other'),
        ('VEHICLE', 'Vehicle'),
        ('JEWELRY', 'Jewelry'),
        ('HOME', 'Home Appliances'),
        ('GARDEN', 'Garden Supplies'),
        ('TOOLS', 'Tools'),
        ('ART_AND_COLLECTIBLES', 'Art & Collectibles'),
        ('PETS_AND_PET_SUPPLIES', 'Pet Supplies'),
    ]
    name = models.CharField(
        max_length=100,
        choices=CATEGORY_TYPES,
        unique=False,
        null=True,
    )
    image = CloudinaryField('image', null=True, blank=True)
    display_name = models.CharField(max_length=100, blank=True, null=True)


    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['-name']
        indexes = [
            models.Index(fields=['name']),
        ]

    def get_display_name(self):
          return dict(self.CATEGORY_TYPES).get(self.name, self.name)

class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    product_name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_featured = models.BooleanField(default=False)
    main_image = CloudinaryField('image', null=True, blank=True) # Using CloudinaryField for image storage
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['-created_at']


class MoreProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField('image', null=True, blank=True) 

    def __str__(self):
        return f"Image for {self.product.product_name}"


