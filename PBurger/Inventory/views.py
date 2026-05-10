from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .models import Stock, Product
from .forms import (
    StockForm,
    ProductBaseForm,
    BurgerExtraForm,
    BeverageExtraForm,
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
    product_form = ProductBaseForm(request.POST or None)
    burger_form = BurgerExtraForm(request.POST or None)
    beverage_form = BeverageExtraForm(request.POST or None)

    p_type = request.POST.get('product_category')
    if request.method == "POST":
        
        if product_form.is_valid():
            
            # Check for Burger
            if p_type == "burger":
                if burger_form.is_valid():
                    burger = burger_form.save(commit=False)
                    burger.name = product_form.cleaned_data["name"]
                    burger.price = product_form.cleaned_data["price"]
                    burger.save()
                    return redirect("stock:produto_inventario")
                else:
                    print(f"Burger Errors: {burger_form.errors}")

            # Check for Beverage
            elif p_type == "beverage":
                if beverage_form.is_valid():
                    beverage = beverage_form.save(commit=False)
                    beverage.name = product_form.cleaned_data["name"]
                    beverage.price = product_form.cleaned_data["price"]
                    beverage.save()
                    return redirect("stock:produto_inventario")
                else:
                    print(f"Beverage Errors: {beverage_form.errors}")
            
            # Catch if p_type is neither
            else:
                print(f"ERROR: p_type received was '{p_type}' - neither burger nor beverage.")

        else:
            print(f"Product Base Errors: {product_form.errors}")

    return render(
        request,
        "product/product_form.html",
        {
            "product_form": product_form,
            "burger_form": burger_form,
            "beverage_form": beverage_form,
        },
    )


@login_required
def update_product_view(request, product_id):
    product_form = ProductBaseForm(request.POST, instance=product_id or None)
    burger_form = BurgerExtraForm(request.POST, instance=product_id or None)
    beverage_form = BeverageExtraForm(request.POST, instance=product_id or None)

    
    if request.method == "POST":
        p_type = request.POST.get('product_category')
    
        if product_form.is_valid():

            if p_type == "burger" and burger_form.is_valid():

                burger = burger_form.save(commit=False)
                burger.name = product_form.cleaned_data["name"]
                burger.price = product_form.cleaned_data["price"]
                burger.save()
                return redirect("stock:produto_inventario")

            elif p_type == "beverage" and beverage_form.is_valid():

                beverage = beverage_form.save(commit=False)
                beverage.name = product_form.cleaned_data["name"]
                beverage.price = product_form.cleaned_data["price"]
                beverage.save()
                return redirect("stock:produto_inventario")
        else:
            print(f"Product Errors: {product_form.errors}")
            print(f"Burger Errors: {burger_form.errors}")
            print(f"Beverage Errors: {beverage_form.errors}")
            return render(
                request,
                "recipe/recipe_form.html",
                status=422,
            )
    
    return render(
        request,
        "product/product_form.html",
        {
            "product_form": product_form,
            "burger_form": burger_form,
            "beverage_form": beverage_form,
        },
    )


@login_required
def delete_product_view(request, product_id):
    item = Product.objects.get(id=product_id)

    if request.method == "POST":
        item.delete()
        return redirect("stock:produto_inventario")

    return render(request, "confirm_delete.html", {"item": item})