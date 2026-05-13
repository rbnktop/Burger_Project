from django.db import models
from Inventory.models import Product
from django.core.validators import MinValueValidator
from simple_history.models import HistoricalRecords
from decimal import Decimal


class Order(models.Model):
    """
    The Receipt Header
    """

    id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal(0),    
        blank=True,
        )
    
    is_processed = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __str__(self):
            return f"Order #{self.id} - {list(self.items.all())} " #type:ignore

    def update_price(self):
        
        # result = self.items.aggregate(
        # total=Sum(F('quantity') * F('product__price'))
        # )

        total = Decimal(0)
        for item in self.items.all():  #type:ignore
            total = item.product.price * item.quantity

        self.total_price += total  #type:ignore
        self.save()


class OrderItem(models.Model):
    """
    The individual lines on the receipt
    """

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.order.update_price()


    def delete(self, *args, **kwargs):
        order = self.order
        deleted_count = super().delete(*args, **kwargs)
        order.update_price()
        return deleted_count
