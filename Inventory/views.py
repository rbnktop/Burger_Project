from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .models import Stock

from .forms import (
    StockForm,
)

def list_stock_view(request):
    stock = Stock.objects.all().prefetch_related("ingredient_items")
    query = request.GET.get("q")
    if query:

        stock = stock.filter(Q(name__icontains=query))
    stock = stock.order_by("name")
    return render(request, "stock_list.html", {"stock": stock})


@login_required
def create_stock_item_view(request):
    form = StockForm()
    if request.method == "POST":
        form = StockForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("stock:inventario")
    return render(request, "stock_form.html", {"form": form})


@login_required
def update_stock_item_view(request, stock_id):
    item = Stock.objects.get(id=stock_id)
    form = StockForm(instance=item)

    if request.method == "POST":
        form = StockForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("stock:inventario")
    return render(request, "stock_form.html", {"form": form})


@login_required
def delete_stock_item_view(request, stock_id):
    item = Stock.objects.get(id=stock_id)

    if request.method == "POST":
        item.delete()
        return redirect("stock:inventario")
    return render(request, "confirm_delete.html", {"item": item})



