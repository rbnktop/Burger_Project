from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from django.db.models import Q

from Burger.settings import LOGIN_URL
import Greeting
from .forms import StockForm, RecipeForm, RecipeRequirementFormSet
from .models import Recipe, Stock


def list_stock_view(request):
    stock = Stock.objects.all()
    query = request.GET.get('q')
    if query:

        stock = stock.filter(
            Q(name__icontains=query)
        )
    stock = stock.order_by('name')
    return render (request, 'stock/stock_list.html', {'stock':stock})

@permission_required('Inventory.add_product', raise_exception=True)
def create_stock_item_view(request):
    form = StockForm()
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('stock:inventario')
    return render(request, 'stock/stock_form.html', {'form':form})

@permission_required('Inventory.add_product', raise_exception=True)
def update_stock_item_view(request, stock_id):
    item = Stock.objects.get(id=stock_id)
    form = StockForm(instance=item)

    if request.method == 'POST':
        form = StockForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect ('stock:inventario')
    return render (request, 'stock/stock_form.html', {'form':form})

@permission_required('Inventory.add_product', raise_exception=True)
def delete_stock_item_view(request, stock_id):
    item = Stock.objects.get(id=stock_id)

    if request.method == 'POST':
        item.delete()
        return redirect('stock:inventario')
    return render (request, 'stock/confirm_delete_stock.html', {'item':item})



def list_recipe_view(request):
    recipe = Recipe.objects.all()
    query = request.GET.get('q')
    if query:

        recipe = recipe.filter(
            Q(name__icontains=query)
        )
    recipe = recipe.order_by('name')
    return render (request, 'recipe/recipe_list.html', {'recipe':recipe})

@permission_required('Inventory.add_product', raise_exception=True)
def create_recipe_view(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        formset = RecipeRequirementFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            recipe = form.save()
            formset.instance = recipe # Link the requirements to the new recipe
            formset.save()
            return redirect('stock:receitaw')
    else:
        form = RecipeForm()
        formset = RecipeRequirementFormSet()

    return render(request, 'recipe/recipe_form.html', {
        'form': form,
        'formset': formset
    })