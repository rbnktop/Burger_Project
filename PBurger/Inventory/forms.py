from django import forms
from .models import Product, Stock, Burger, Beverage

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
