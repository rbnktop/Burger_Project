from django import forms
from .models import Burger, Beverage, Recipe, Stock


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


class BurgerForm(forms.ModelForm):
    product_category = forms.ChoiceField(
        choices=[("burger", "Hambúrguer"), ("beverage", "Bebida")],
        widget=forms.RadioSelect(attrs={"class": "category-radio"}),
        initial=None,
    )

    class Meta:
        model = Burger
        fields = ["name", "price", "product_category", "description", "image"]
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


class BeverageForm(forms.ModelForm):
    class Meta:
        model = Beverage
        fields = ["name", "price", "stock", "image", "description"]
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
                    "placeholder": "A parte",
                }
            ),
            "image": forms.FileInput(),
            "stock": forms.Select(
                attrs={"class": "form-select text-white border-secondary"}
            ),
        }


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
                    "placeholder": "Qtd",
                }
            ),
        }
