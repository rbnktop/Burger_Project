from functools import Placeholder
from os import name

from django import forms
from .models import Stock, Recipe, RecipeRequirements, Burger, Beverage


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = '__all__'
        labels = {
            'name' : 'Nome Produto', 
            'quantity' : 'Quantidade',
            'price' : 'Preço',
            'unit' : 'Unidade de Medida'
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Cebola'
            }),
            'quantity' : forms.NumberInput(attrs={
                'placeholder': '20'
            }),
            'unit': forms.ChoiceField(choices=Stock.UNIT_CHOICES),
            # 'price': forms.FloatField(),
        }