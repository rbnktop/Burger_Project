from django import forms
from django.forms import inlineformset_factory
from django.forms.models import BaseInlineFormSet

from .models import Recipe, RecipeItems
from Inventory.models import Stock


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nome da Receita"}
            ),
        }


class BaseRecipeItemsFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        queryset = Stock.objects.all()
        for form in self.forms:
            if "ingredient" in form.fields:
                form.fields["ingredient"].queryset = queryset  # type: ignore pylance doesnt see the ingredient as a modelchoicefield

RecipeItemsFormSet = inlineformset_factory(
    Recipe,
    RecipeItems,
    formset=BaseRecipeItemsFormSet,
    fields=["ingredient", "amount"],
    extra=2,
    can_delete=True,
    widgets={
        "ingredient": forms.Select(
            attrs={
                "class": "form-select",
                "placeholder": "Cebolinha",
            }
        ),
        "amount": forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "15.7"}
        ),
    },
)
