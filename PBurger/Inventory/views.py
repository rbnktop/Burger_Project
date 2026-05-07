from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required

from Burger.settings import LOGIN_URL
import Greeting
from .forms import StockForm
from .models import Stock


def list_stock_view(request):
    stock = Stock.objects.all()
    return render (request, 'stock_list.html', {'stock':stock})

@permission_required('Inventory.add_product', raise_exception=True)
def create_stock_item_view(request):
    form = StockForm()
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('stock:inventario')
    return render(request, 'stock_form.html', {'form':form})

@permission_required('Inventory.add_product', raise_exception=True)
def update_stock_item_view(request, stock_id):
    item = Stock.objects.get(id=stock_id)
    form = StockForm(instance=item)

    if request.method == 'POST':
        form = StockForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect ('stock:inventario')
    return render (request, 'stock_form.html', {'form':form})

@permission_required('Inventory.add_product', raise_exception=True)
def delete_stock_item_view(request, stock_id):
    item = Stock.objects.get(id=stock_id)

    if request.method == 'POST':
        item.delete()
        return redirect('stock:inventario')
    return render (request, 'confirm_delete_stock.html', {'item':item})