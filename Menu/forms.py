from .models import Dish, NonDish, Recipe
from django.forms import inlineformset_factory
from django import forms
from .models import Category 
from typing import cast


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
    new_category = forms.CharField(
        required=False,
        label= "criar nova",
        widget=forms.TextInput(
            attrs={
                "class":"form-control text-white border-secondary",
                "placeholder":"Batatas/Lanche",
                })
    )

    class Meta:
        model = Dish
        fields = ["product_base_category", "category", "name", "price", "description", "image"]
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "category" in self.fields:
            category_field = cast(forms.ModelChoiceField, self.fields["category"])
            category_field.queryset = Category.objects.filter(category_type="DISH")
            category_field.widget.attrs.update({"class": "form-select text-white border-secondary"})
            category_field.label = "Categoria"


    def save(self, commit=True):
        # Fat Form Practice: Intercept the save chain to build the category behind the scenes
        instance = super().save(commit=False)
        new_cat = self.cleaned_data.get("new_category")
        
        if new_cat:
            from .models import Category
            category_obj, _ = Category.objects.get_or_create(
                name=new_cat.strip(),
                category_type="DISH"
            )
            instance.category = category_obj
            
        if commit:
            instance.save()
        return instance



class NonDishForm(BaseProductForm):
    new_category = forms.CharField(
        required=False,
        label = "criar nova",
        widget=forms.TextInput(
            attrs={
                "class":"form-control",
                "placeholder":"Cervejas/Doces"})
    )

    class Meta:
        model = NonDish
        fields = ["product_base_category", "category", "name", "price", "stock", "image", "description"]
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "category" in self.fields:
            category_field = cast(forms.ModelChoiceField, self.fields["category"])
            category_field.queryset = Category.objects.filter(category_type="NONDISH")
            category_field.widget.attrs.update({"class": "form-select text-white border-secondary"})
            category_field.label = "Categoria"

    def save(self, commit=True):
        instance = super().save(commit=False)
        new_cat = self.cleaned_data.get("new_category")
        
        if new_cat:
            from .models import Category
            category_obj, _ = Category.objects.get_or_create(
                name=new_cat.strip(),
                category_type="NONDISH"
            )
            instance.category = category_obj
            
        if commit:
            instance.save()
        return instance