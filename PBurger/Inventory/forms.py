from django import forms
from .models import Stock, Recipe, RecipeRequirements, Burger, Beverage
from django.forms import inlineformset_factory
from django.forms.models import BaseInlineFormSet

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

class BaseRecipeRequirementFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Fetch the ingredients ONCE
        queryset = Stock.objects.all() 
        for form in self.forms:
            if 'ingredient' in form.fields:
                form.fields['ingredient'].queryset = queryset

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
    formset=BaseRecipeRequirementFormSet,  # <--- THIS IS THE ONLY CHANGE
    fields=["ingredient", "amount"],
    extra=4,
    can_delete=True,
    widgets={
        "ingredient": forms.Select(
            attrs={"class": "form-select", "placeholder": "Cebolinha"}
        ),
        "amount": forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "15.7"}
        ),
    },
)

