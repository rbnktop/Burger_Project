
from django.db import models
from Inventory.models import Product 

class Order(models.Model):
    """
    The Receipt Header
    """
    id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.FloatField(default=0.0)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"

class OrderItem(models.Model):
    """
    The individual lines on the receipt (e.g., 2x Classic Burger)
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"