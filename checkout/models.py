import uuid
from django.db import models
from django.db.models import Sum
from products.models import Product
from django.conf import settings

# Create your models here.
class Order(models.Model):
    order_number = models.CharField( unique=True, editable=False, default=0)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    post_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Order {self.id} by {self.first_name} {self.last_name}"
    
    def _generate_order_number(self):
        return uuid.uuid4().hex.upper()
    
    def calculate_order_total(self):
        self.order_total = self.order_items.aggregate(Sum('orderitem_total'))['orderitem_total__sum'] or 0
        self.grand_total = self.order_total + settings.DELIVERY_CHARGE
        self.save()
        

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    orderitem_total = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return f"{self.product.name} (Order {self.order.order_number})"
    
    def save(self, *args, **kwargs):
        self.orderitem_total = self.price * self.quantity
        super().save(*args, **kwargs)

    def calculate_orderitem_total(self):
        self.orderitem_total = self.price * self.quantity
        self.save()