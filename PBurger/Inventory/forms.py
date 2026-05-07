from django import forms
from .models import Stock, Recipe, RecipeRequirements, Burger, Beverage
from django.forms import inlineformset_factory


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = "__all__"
        labels = {
            "name": "Nome Produto",
            "quantity": "Quantidade",
            "unit": "Unidade de Medida",
            "price": "Valor",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Cebola",
                    "class": "form-control",
                }
            ),
            "quantity": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "20",
                    "min": "0.01",
                }
            ),
            "unit": forms.Select(
                attrs={
                    "class": "Unit_Choices",
                    "class": "form-control",
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "2.50",
                    "min": "0.5",
                }
            ),
        }


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nome da Receita"}
            ),
        }


# This creates a set of forms for RecipeRequirements linked to one Recipe
RecipeRequirementFormSet = inlineformset_factory(
    Recipe,
    RecipeRequirements,
    fields=["ingredient", "amount"],
    extra=4,
    can_delete=True,
    widgets={
        "ingredient": forms.Select(
            attrs={"class": "form-control", "placeholder": "Cebola"}
        ),
        "amount": forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "0.0"}
        ),
    },
)
