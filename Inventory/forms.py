from django import forms
from .models import Stock


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


