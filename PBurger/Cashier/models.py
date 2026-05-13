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
    customer_name = models.CharField(max_length=100, blank=True, null=True, default="Cliente")
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal(0),    
        blank=True,
        )
    
    status = models.BooleanField(default=False)

    history = HistoricalRecords()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        items_summary = ", ".join([str(item) for item in self.items.all()])  #type:ignore
        return f"{self.id}° ${self.total_price} {items_summary} " #type:ignore

    def update_price(self):
        
        # result = self.items.aggregate(
        # total=Sum(F('quantity') * F('product__price'))
        # )

        total = Decimal(0)
        for item in self.items.all():  #type:ignore
            total = item.product.price * item.quantity

        self.total_price += total 
        self.save()


class OrderItem(models.Model):
    """
    The individual lines on the receipt
    """

    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
    
        if is_new:
            self.product.update_stock(self.quantity) 
            self.order.update_price()

    def delete(self, *args, **kwargs):
        if self.product:
            self.product.update_stock(-self.quantity)

        order = self.order
        deleted_count = super().delete(*args, **kwargs)

        if order:
            order.update_price()
        return deleted_count
