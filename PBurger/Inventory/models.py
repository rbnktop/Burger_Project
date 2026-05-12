from unicodedata import decimal

from django.db import models
from django.core.validators import MinValueValidator



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
    quantity = models.FloatField(validators=[MinValueValidator(0.01)], blank=False)
    image = models.ImageField(upload_to='stock/', null=True, blank=True)
    unit = models.CharField(max_length=8, choices=UNIT_CHOICES, blank=False)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)], blank=False
    )
    create_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.quantity}{self.unit}"


class Product(models.Model):
    """
    Base product
    """

    name = models.CharField(max_length=32, unique=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)], blank=False
    )    
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='product/', null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    sold = models.IntegerField()

    def __str__(self):
        return f" Produto: {self.name} ID: {self.id} por R${self.price}" #type:ignore


class Burger(Product):
    """
    Child product with a recipe
    """

    ingredients = models.ManyToManyField('Inventory.Stock', through='Recipe')

    def update_stock(self, quantity_sold):
        self.sold =+ quantity_sold
        for item in self.recipe_items.all(): #type:ignore
            item.ingredient.quantity -= item.amount * quantity_sold
            item.ingredient.save()


    def get_total_cost(self):
        total_cost = 0
        for item in self.recipe_items.all(): #type:ignore
            total_cost += int((item.amount * float(item.ingredient.price)))
        return round(total_cost, 2)
    
    @property
    def profit_margin(self):
        """
        Calculates how much you make after production costs.
        """
        cost = self.get_total_cost()
        return round(self.price - cost, 2)


class Recipe(models.Model):
    """
    Recipe of the meal
    """

    burger = models.ForeignKey(Burger, on_delete=models.CASCADE, related_name="recipe_items")
    ingredient = models.ForeignKey(Stock, on_delete=models.PROTECT)
    amount = models.FloatField()

    def __str__(self):
        return f" Receita: {self.burger} ID: {self.id} precisa de {self.amount}{self.ingredient.unit} {self.ingredient.name}" #type:ignore


class Beverage(Product):
    """
    Child product with no recipe
    """

    stock = models.ForeignKey(Stock, on_delete=models.PROTECT)

    def __str__(self):
        return f" {self.name} R${self.price}"
    
    def update_stock(self, quantity_sold):
        self.stock.quantity -= quantity_sold
        self.stock.save()

    @property
    def profit_margin(self):
        """
        Calculates how much you make after production costs.
        """
        return round(self.price - self.stock.price, 2)