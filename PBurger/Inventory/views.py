from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .models import Recipe, Stock
from .forms import StockForm, RecipeForm, RecipeRequirementFormSet


def list_stock_view(request):
    stock = Stock.objects.all()
    query = request.GET.get("q")
    if query:

        stock = stock.filter(Q(name__icontains=query))
    stock = stock.order_by("name")
    return render(request, "stock/stock_list.html", {"stock": stock})

@login_required
def create_stock_item_view(request):
    form = StockForm()
    if request.method == "POST":
        form = StockForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("stock:inventario")
    return render(request, "stock/stock_form.html", {"form": form})

@login_required
def update_stock_item_view(request, stock_id):
    item = Stock.objects.get(id=stock_id)
    form = StockForm(instance=item)

    if request.method == "POST":
        form = StockForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("stock:inventario")
    return render(request, "stock/stock_form.html", {"form": form})

@login_required
def delete_stock_item_view(request, stock_id):
    item = Stock.objects.get(id=stock_id)

    if request.method == "POST":
        item.delete()
        return redirect("stock:inventario")
    return render(request, "stock/confirm_delete_stock.html", {"item": item})


# recipes

def list_recipe_view(request):
    recipe = Recipe.objects.all()
    query = request.GET.get("q")
    if query:
        recipe = recipe.filter(Q(name__icontains=query))
    recipe = recipe.order_by("name")

    return render(request, "recipe/recipe_list.html", {"recipe": recipe})

@login_required
def update_recipe_view(request, recipe_id):
    item = get_object_or_404(Recipe.objects.prefetch_related('requirements'), id=recipe_id)

    if request.method == "POST":
        form = RecipeForm(request.POST, instance=item)
        formset = RecipeRequirementFormSet(request.POST, instance=item)
        print(f"Form errors: {form.errors}")
        print(f"Formset errors: {formset.errors}")
        if form.is_valid() and formset.is_valid():
            print('valid')
            recipe = form.save()
            formset.instance = recipe
            formset.save()
            return redirect("stock:receita_inventario")
        else: 
            return render(request, "recipe/recipe_form.html", {"form": form, "formset": formset}, status=422)
    else:

        form = RecipeForm(instance=item)
        formset = RecipeRequirementFormSet(instance=item)
    return render(
        request, "recipe/recipe_form.html", {"form": form, "formset": formset}
    )

@login_required
def create_recipe_view(request):
    if request.method == "POST":
        form = RecipeForm(request.POST)
        formset = RecipeRequirementFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            recipe = form.save()
            formset.instance = recipe
            formset.save()
            return redirect("stock:receita_inventario")
        else: print(f"{form.errors}")
    else:
        form = RecipeForm()
        formset = RecipeRequirementFormSet()

    return render(
        request, "recipe/recipe_form.html", {"form": form, "formset": formset}
    )

@login_required
def delete_recipe_view(request, stock_id):
    item = Recipe.objects.get(id=stock_id)

    if request.method == "POST":
        item.delete()
        return redirect("stock:receita_inventario")
    return render(request, "recipe/confirm_delete_recipe.html", {"item": item})
