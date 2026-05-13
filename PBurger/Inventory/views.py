from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.forms import inlineformset_factory

from .models import Recipe, Burger, Beverage, Product, Stock

from .forms import (
    StockForm,
    BurgerForm,
    BeverageForm,
    RecipeForm,
)

RecipeFormSet = inlineformset_factory(
    Burger, Recipe, fields=("ingredient", "amount"), extra=2, can_delete=True
)


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
    return render(request, "confirm_delete.html", {"item": item})





def list_product_view(request):
    product = Product.objects.all()
    query = request.GET.get("q")

    if query:
        product = product.filter(Q(name__icontains=query))

    product = product.order_by("name")

    return render(request, "product/product_list.html", {"product": product})


@login_required
def create_product_view(request):
    form = BurgerForm()
    formset = RecipeFormSet()
    beverage_form = BeverageForm()
    product_category = "None"

    if request.method == "POST":
        product_category = request.POST.get("product_category", "None")
        print(f"--- DEBUG product type: {product_category} ---")

        if product_category == "burger":
            form = BurgerForm(request.POST, request.FILES)
            formset = RecipeFormSet(request.POST)

            if form.is_valid() and formset.is_valid():
                burger = form.save()
                formset.instance = burger
                formset.save()
                return redirect("stock:produto_inventario")
            else:
                if not form.is_valid():
                    print("FORM ERRORS:", form.errors.as_json())
                if not formset.is_valid():
                    print("FORMSET ERRORS:", formset.errors)

        elif product_category == "beverage":
            beverage_form = BeverageForm(request.POST, request.FILES)
            if beverage_form.is_valid():
                beverage_form.save()
                return redirect("stock:produto_inventario")
            else:
                print("BEVERAGE ERRORS:", beverage_form.errors)

    common_form = beverage_form if product_category == "beverage" else form

    return render(
        request,
        "product/product_form.html",
        {
            "form": form,
            "formset": formset,
            "beverage_form": beverage_form,
            "common_form": common_form,
            "product_category": product_category,
        },
        status=422 if request.method == "POST" else 200,
    )


@login_required
def update_product_view(request, product_id):
    product_obj = get_object_or_404(Product, id=product_id)

    if hasattr(product_obj, "burger"):
        item = product_obj.burger  # type: ignore
        product_category = "burger"
    elif hasattr(product_obj, "beverage"):
        item = product_obj.beverage  # type: ignore
        product_category = "beverage"
    else:
        item = product_obj
        product_category = "None"

    form = BurgerForm(instance=item if product_category == "burger" else None)
    formset = RecipeFormSet(instance=item if product_category == "burger" else None)
    beverage_form = BeverageForm(
        instance=item if product_category == "beverage" else None
    )

    if request.method == "POST":
        product_category = request.POST.get("product_category")

        if product_category == "burger":
            form = BurgerForm(request.POST, request.FILES, instance=item)
            formset = RecipeFormSet(request.POST, instance=item)

            if form.is_valid() and formset.is_valid():
                burger = form.save()
                formset.instance = burger
                formset.save()
                return redirect("stock:produto_inventario")

            else:
                if not form.is_valid():
                    print("FORM ERRORS:", form.errors.as_json())
                if not formset.is_valid():
                    print("FORMSET ERRORS:", formset.errors)

        elif product_category == "beverage":
            beverage_form = BeverageForm(request.POST, request.FILES, instance=item)

            if beverage_form.is_valid():
                beverage_form.save()
                return redirect("stock:produto_inventario")

            else:
                print("BEVERAGE ERRORS:", beverage_form.errors)

    common_form = beverage_form if product_category == "beverage" else form

    return render(
        request,
        "product/product_form.html",
        {
            "form": form,
            "formset": formset,
            "beverage_form": beverage_form,
            "common_form": common_form,
            "product_category": product_category,
        },
    )


@login_required
def delete_product_view(request, product_id):
    item = Product.objects.get(id=product_id)

    if request.method == "POST":
        item.delete()
        return redirect("stock:produto_inventario")

    return render(request, "confirm_delete.html", {"item": item})
