from django import forms
from .models import Dish, NonDish, Recipe, Stock
from django.forms import inlineformset_factory


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = "__all__"
        labels = {
            "name": "Nome Item",
            "quantity": "Quantidade",
            "unit": "Unidade de Medida",
            "price": "Valor",
            "image": "Imagem",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Cebola",
                    "class": "form-control",
                }
            ),
            "quantity": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "200",
                    "min": "0.01",
                }
            ),
            "unit": forms.Select(
                attrs={
                    "class": "Unit_Choices",
                    "class": "form-control",
                    "placeholder": "fatias",
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "$25.80",
                    "min": "0.5",
                }
            ),
            "image": forms.FileInput(),
        }


class BaseProductForm(forms.ModelForm):
    product_base_category = forms.ChoiceField(
        choices=[("dish", "Cozinha"), ("nondish", "Outros")],
        widget=forms.RadioSelect(attrs={"class": "category-radio"}),
        initial=None,
        required=True,
    )


RecipeFormSet = inlineformset_factory(
    Dish, 
    Recipe, 
    fields=("ingredient", "amount"), 
    extra=2, 
    can_delete=True,
    min_num=1,
    validate_min=True,
)


class RecipeForm(forms.ModelForm):
    """
    This form will be used inside the FormSet for each ingredient row
    """

    class Meta:
        model = Recipe
        fields = ["ingredient", "amount"]
        widgets = {
            "ingredient": forms.Select(
                attrs={"class": "form-select text-white border-secondary flex-grow-1"}
            ),
            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control text-white border-secondary",
                    "style": "width: 100px;",
                    "placeholder": "somente numeros",
                }
            ),
        }


class DishForm(BaseProductForm):
    class Meta:
        model = Dish
        fields = ["product_base_category", "name", "price", "description", "image"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control text-white border-secondary",
                    "placeholder": "X-Salada",
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": "form-control text-white border-secondary",
                    "placeholder": "$4.21",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-select text-white border-secondary",
                    "placeholder": "Um lanche muito daora mesmo",
                }
            ),
            "image": forms.FileInput(),
        }


class OtherForm(BaseProductForm):
    class Meta:
        model = NonDish
        fields = ["product_base_category", "name", "price", "stock", "image", "description"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control text-white border-secondary",
                    "placeholder": "Coca lata",
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": "form-control text-white border-secondary",
                    "placeholder": "$4.21",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control text-white border-secondary",
                    "placeholder": "Uma latinha de refrigerante.",
                }
            ),
            "image": forms.FileInput(),
            "stock": forms.Select(
                attrs={"class": "form-select text-white border-secondary"}
            ),
        }
