from django.shortcuts import render, redirect
from .forms import StockForm
from .models import Stock


def list_stock_view(request):
    stock = Stock.objects.all()
    return render (request, 'stock_list.html', {'stock':stock})


def create_stock_item_view(request):
    form = StockForm()
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('stock_list.html')
    return redirect(request, 'stock_form.html', {'form':form})


def update_stock_item_view(request, stock_id):
    item = Stock.objects.get(stock_id=stock_id)
    form = StockForm(instance=item)

    if request.method == 'POST':
        form = StockForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect ('stock_list.html')
    return redirect (request, 'stock_form.html', {'form':form})


def delete_stock_item_view(request, stock_id):
    item = Stock.objects.get(stock_id=stock_id)

    if request.method == 'POST':
        item.delete()
        return redirect('stock_list.html')
    return render (request, 'confirm_delete_stock.html', {'stock':item})