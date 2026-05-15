from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .models import Product, Stock

from .forms import (
    DishForm,
    OtherForm,
    RecipeFormSet,
)


def list_product_view(request):
    products = Product.objects.all().prefetch_related(
        "dish__recipe_items__ingredient", "nondish__stock"
    )

    query = request.GET.get("q")

    if query:
        products = products.filter(Q(name__icontains=query))

    products = products.order_by("-total_sold")

    return render(request, "product_list.html", {"products": products})

@login_required
def create_product_view(request):
    form = DishForm()
    formset = RecipeFormSet()
    nondish_form = OtherForm()
    product_base_category = "None"

    if request.method == "POST":
        product_base_category = request.POST.get("product_base_category", "None")
        print(f"--- DEBUG product type: {product_base_category} ---")

        if product_base_category == "dish":
            form = DishForm(request.POST, request.FILES)
            formset = RecipeFormSet(request.POST)

            if form.is_valid() and formset.is_valid():
                dish = form.save()
                formset.instance = dish
                formset.save()
                return redirect("stock:produto_inventario")
            else:
                if not form.is_valid():
                    print("FORM ERRORS:", form.errors.as_json())
                if not formset.is_valid():
                    print("FORMSET ERRORS:", formset.errors)

        elif product_base_category == "nondish":
            nondish_form = OtherForm(request.POST, request.FILES)

            if nondish_form.is_valid():
                nondish_form.save()
                return redirect("stock:produto_inventario")
            else:
                print("NONDISH ERRORS:", nondish_form.errors)

    common_form = nondish_form if product_base_category == "nondish" else form

    context = {
        "form": form,
        "formset": formset,
        "nondish_form": nondish_form,
        "common_form": common_form,
        "product_base_category": product_base_category,
    }

    return render(
        request,
        "product_form.html",
        context,
        status=422 if request.method == "POST" else 200,
    )


@login_required
def update_product_view(request, product_id):
    product_obj = get_object_or_404(Product, id=product_id)

    if hasattr(product_obj, "dish"):
        item = product_obj.dish  # type: ignore
        product_base_category = "dish"
    elif hasattr(product_obj, "nondish"):
        item = product_obj.nondish  # type: ignore
        product_base_category = "nondish"
    else:
        item = product_obj
        product_base_category = "None"

    form = DishForm(instance=item if product_base_category == "dish" else None)
    formset = RecipeFormSet(instance=item if product_base_category == "dish" else None)
    nondish_form = OtherForm(instance=item if product_base_category == "nondish" else None)

    if request.method == "POST":
        posted_category = request.POST.get("product_base_category")

        if product_base_category == "dish":
            form = DishForm(request.POST, request.FILES, instance=item)
            formset = RecipeFormSet(request.POST, instance=item)

            if form.is_valid() and formset.is_valid():
                dish = form.save()
                formset.instance = dish
                formset.save()
                return redirect("stock:produto_inventario")

            else:
                if not form.is_valid():
                    print("FORM ERRORS:", form.errors.as_json())
                if not formset.is_valid():
                    print("FORMSET ERRORS:", formset.errors)

        elif product_base_category == "nondish":
            nondish_form = OtherForm(request.POST, request.FILES, instance=item)

            if nondish_form.is_valid():
                nondish_form.save()
                return redirect("stock:produto_inventario")

            else:
                print("NONDISH ERRORS:", nondish_form.errors)

    common_form = nondish_form if product_base_category == "nondish" else form

    return render(
        request,
        "product_form.html",
        {
            "form": form,
            "formset": formset,
            "nondish_form": nondish_form,
            "common_form": common_form,
            "product_base_category": product_base_category,
        },
    )


@login_required
def delete_product_view(request, product_id):
    item = Product.objects.get(id=product_id)

    if request.method == "POST":
        item.delete()
        return redirect("stock:produto_inventario")

    return render(request, "confirm_delete.html", {"item": item})