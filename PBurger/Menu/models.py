from django.db import models
from django.core.validators import MinValueValidator
from simple_history.models import HistoricalRecords
from polymorphic.models import PolymorphicModel
from abc import abstractmethod
from Inventory.models import Stock


class Product(PolymorphicModel):
    """
    Base product
    """

    name = models.CharField(max_length=32, unique=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        blank=False,
    )
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="product/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_sold = models.IntegerField(default=0)
    history = HistoricalRecords(inherit=True)

    def __str__(self):
        return f"{self.name} ${self.price}"  # type: ignore [{self.id}]

    @abstractmethod
    def update_stock(self, quantity_sold):
        pass


class Dish(Product):
    """
    Child product with a recipe
    """

    ingredients = models.ManyToManyField("Inventory.Stock", through="Recipe")

    def update_stock(self, quantity_sold):
        self.total_sold += quantity_sold
        self.save(update_fields=["total_sold"])

        for item in self.recipe_items.all():  # type: ignore
            item.ingredient.quantity -= item.amount * quantity_sold
            item.ingredient.save()

    def get_total_cost(self):
        total_cost = 0
        for item in self.recipe_items.all():  # type: ignore
            if item.ingredient.unit == "g":
                price = item.ingredient.price / 1000
                total_cost += int((item.amount * float(price)))
            else:
                total_cost += int((item.amount * float(item.ingredient.price)))
        return total_cost

    @property
    def profit(self):
        """
        Calculates how much you make after production costs.
        """
        cost = self.get_total_cost()
        return self.price - cost


class NonDish(Product):
    """
    Child product with no recipe
    """

    stock = models.ForeignKey(Stock, on_delete=models.PROTECT)

    def __str__(self):
        return f" {self.name} R${self.price} ."

    def update_stock(self, quantity_sold):
        self.total_sold += quantity_sold
        self.save(update_fields=["total_sold"])
        self.stock.quantity -= quantity_sold
        self.stock.save()

    @property
    def profit_margin(self):
        """
        Calculates how much you make after production costs.
        """
        return self.price - self.stock.price


class Recipe(models.Model):
    """
    Recipe of the meal
    """

    dish = models.ForeignKey(
        Dish, on_delete=models.CASCADE, related_name="recipe_items"
    )
    ingredient = models.ForeignKey(
        Stock, on_delete=models.PROTECT, related_name="ingredient_items"
    )
    amount = models.FloatField()

    def __str__(self):
        return f"{self.amount}{self.ingredient.unit} {self.ingredient.name}"  # type: ignore


        