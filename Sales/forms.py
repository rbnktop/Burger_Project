from django import forms
from django.forms import inlineformset_factory

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
                    "placeholder": "Fulano",
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


OrderItemFormSet = inlineformset_factory(
    Order, OrderItem,
    fields=("product", "quantity"), 
    can_delete=True, 
    extra=0, 
)
