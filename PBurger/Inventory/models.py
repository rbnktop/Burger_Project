from django.db import models
from django.core.validators import MinValueValidator

from Recipe.models import Recipe, RecipeItems


class Stock(models.Model):
    """
    Stock Items, including ingredients beverages and such
    """

    UNIT_CHOICES = [
        ("g", "Gramas"),
        ("ml", "Mililitros"),
        ("un", "Unidades/Fatias"),
    ]

    name = models.CharField(max_length=32, unique=True)
    quantity = models.FloatField(validators=[MinValueValidator(0.01)])
    unit = models.CharField(max_length=8, choices=UNIT_CHOICES)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)]
    )

    def __str__(self):
        return f"{self.name} - {self.quantity}{self.unit}"


class Product(models.Model):
    """
    Base product
    """

    name = models.CharField(max_length=32, unique=True)
    price = models.FloatField()

    def __str__(self):
        return f" Produto: {self.name} por R${self.price}"


class Burger(Product):
    """
    Child product with a recipe
    """

    recipe = models.ForeignKey(Recipe, on_delete=models.PROTECT)

    def update_stock(self, quantity_sold):
        ingredients = RecipeItems.objects.filter(recipe=self.recipe)

        for i in ingredients:
            i.ingredient.quantity -= i.amount * quantity_sold
            i.ingredient.save()

    def __str__(self):
        return f" Burger: {self.name} por R${self.price}"


class Beverage(Product):
    """
    Child product with no recipe
    """

    stock = models.ForeignKey(Stock, on_delete=models.PROTECT)

    def update_stock(self, quantity_sold):
        self.stock.quantity -= quantity_sold
        self.stock.save()

    def __str__(self):
        return f" Bebida: {self.name} por R${self.price}"
