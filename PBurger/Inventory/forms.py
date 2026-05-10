from django import forms
from .models import Product, Stock, Recipe, RecipeItems, Burger, Beverage
from django.forms import inlineformset_factory
from django.forms.models import BaseInlineFormSet


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = "__all__"
        labels = {
            "name": "Nome Item",
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


class ProductBaseForm(forms.ModelForm):
    ProductCategories = [
        ("burger", "Hambúrguer"),
        ("beverage", "Bebida"),
    ]
    # Adding Bootstrap classes to the widget
    product_category = forms.ChoiceField(
        choices=ProductCategories,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
    )

    class Meta:
        model = Product
        fields = ["name", "price"]


class BurgerExtraForm(forms.ModelForm):
    class Meta:
        model = Burger
        fields = ["recipe"]


class BeverageExtraForm(forms.ModelForm):
    class Meta:
        model = Beverage
        fields = ["stock"]
