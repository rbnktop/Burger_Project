from django import forms
from .models import Stock, Recipe, RecipeRequirements, Burger, Beverage


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = '__all__'
        labels = {
            'name' : 'Nome Produto', 
            'quantity' : 'Quantidade',
            'unit' : 'Unidade de Medida',
            'price' : 'Preço',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Cebola',
                'class': 'form-control',
            }),
            'quantity' : forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '20',
                'min': '0.01', 
            }),
            'unit': forms.Select(attrs={
                'class':'Unit_Choices',
                'class': 'form-control',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': '2.50',    
                'min': '0.5',              
            }),
        }

