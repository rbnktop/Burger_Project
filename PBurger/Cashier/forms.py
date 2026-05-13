from django import forms
from .models import Order, OrderItem

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "__all__"
        labels = {
            "customer_name": "Cliente",
        }
        widgets = {
            "customer_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "mae do andy",
                    "class": "form-control",
                }
            )
        }

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]
        widgets = {
            "product": forms.Select(
                attrs={"class": "form-select text-white border-secondary flex-grow-1"}
            ),
            "quantity": forms.NumberInput(
                attrs={
                    "class": "form-control text-white border-secondary",
                    "style": "width: 100px;",
                    "placeholder": "Qtd",
                }
            ),
        }

