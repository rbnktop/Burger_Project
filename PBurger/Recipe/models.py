from django.db import models


class Recipe(models.Model):
    """
    Recipe of the meal
    """

    name = models.CharField(max_length=32, unique=True)
    ingredients = models.ManyToManyField('Inventory.Stock', through="RecipeItems")

    def __str__(self):
        return f"{self.name}"


class RecipeItems(models.Model):
    """
    Amount of ingredients required to cook
    """

    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="requirements"
    )
    ingredient = models.ForeignKey('Inventory.Stock', on_delete=models.PROTECT)
    amount = models.FloatField()

    def __str__(self):
        return f" Receita: {self.recipe.name} precisa de {self.amount}{self.ingredient.unit} {self.ingredient.name}"