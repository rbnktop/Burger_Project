from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .models import Recipe

from .forms import (
    RecipeForm,
    RecipeItemsFormSet,
)



def list_recipe_view(request):
    recipe = Recipe.objects.all()
    query = request.GET.get("q")
    if query:
        recipe = recipe.filter(Q(name__icontains=query))
    recipe = recipe.order_by("name")

    return render(request, "recipe/recipe_list.html", {"recipe": recipe})


@login_required
def create_recipe_view(request):
    if request.method == "POST":
        form = RecipeForm(request.POST)
        formset = RecipeItemsFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            recipe = form.save()
            formset.instance = recipe
            formset.save()
            return redirect("recipe:receita_inventario")
        else:
            print(f"{form.errors}")
    else:
        form = RecipeForm()
        formset = RecipeItemsFormSet()

    return render(
        request, "recipe/recipe_form.html", {"form": form, "formset": formset}
    )


@login_required
def update_recipe_view(request, recipe_id):
    item = get_object_or_404(
        Recipe.objects.prefetch_related("requirements"), id=recipe_id
    )

    if request.method == "POST":
        form = RecipeForm(request.POST, instance=item)
        formset = RecipeItemsFormSet(request.POST, instance=item)
        print(f"Form errors: {form.errors}")
        print(f"Formset errors: {formset.errors}")
        if form.is_valid() and formset.is_valid():
            print("valid")
            recipe = form.save()
            formset.instance = recipe
            formset.save()
            return redirect("recipe:receita_inventario")
        else:
            return render(
                request,
                "recipe/recipe_form.html",
                {"form": form, "formset": formset},
                status=422,
            )
    else:

        form = RecipeForm(instance=item)
        formset = RecipeItemsFormSet(instance=item)

    return render(
        request, "recipe/recipe_form.html", {"form": form, "formset": formset}
    )


@login_required
def delete_recipe_view(request, recipe_id):
    item = Recipe.objects.get(id=recipe_id)

    if request.method == "POST":
        item.delete()
        return redirect("recipe:receita_inventario")

    return render(request, "confirm_delete.html", {"item": item})
