from django.db import models
from django.core.validators import MinValueValidator
from simple_history.models import HistoricalRecords



class Stock(models.Model):
    """
    Stock Items, including ingredients nondishs and such
    """

    UNIT_CHOICES = [
        ("g", "Gramas"),
        ("ml", "Mililitros"),
        ("un", "Unidades"),
    ]

    name = models.CharField(max_length=32, unique=True)
    quantity = models.FloatField(validators=[MinValueValidator(0.01)], blank=False)
    unit = models.CharField(max_length=8, choices=UNIT_CHOICES, blank=False)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        blank=False,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="stock/", null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return f" {self.name} | {self.quantity}{self.unit}"  # type: ignore [{self.id}]

    @property
    def quantity_display(self):
        """Returns a string with the best unit for display"""
        if self.unit == "g" and self.quantity >= 1000:
            kg_val: float = self.quantity / 1000
            return kg_val
        return self.quantity

    @property
    def unit_display(self):
        if self.unit == "g" and self.quantity >= 1000:
            return "Kg"
        else:
            return self.unit



