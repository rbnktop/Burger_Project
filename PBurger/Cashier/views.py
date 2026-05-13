import json
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.db import transaction
from decimal import Decimal
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .services import validate_cart_stock
from Inventory.models import Beverage, Burger, Stock
from .models import Order, OrderItem
from .forms import OrderForm

OrderItemFormSet = inlineformset_factory(
        Order, 
        OrderItem, 
        fields=('product', 'quantity'),
        extra=1, 
        can_delete=True
    )




def hub_view(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST)

        if form.is_valid():
            order = form.save()
            formset = OrderItemFormSet(request.POST, instance=order)
            if formset.is_valid():
                formset.save()
                return redirect('cashier:hub')
   
    else:
        form = OrderForm()
        formset = OrderItemFormSet()

    return render(request, 'hub.html', {
        'form': form,
        'formset': formset,
    })

def calculate_order_total(request):
    """
    Calculates the total on-the-fly using only POST data. 
    Does not require the Order to exist in the DB yet.
    """
    # Initialize the formset with POST data but NO instance
    formset = OrderItemFormSet(request.POST)
    
    total = Decimal('0.00')
    
    # We don't necessarily need formset.is_valid() just to calculate a preview total,
    # but it's safer to use cleaned_data.
    if formset.is_valid():
        for form in formset:
            # Check if it's not marked for deletion
            if not form.cleaned_data.get('DELETE'):
                product = form.cleaned_data.get('product')
                quantity = form.cleaned_data.get('quantity', 0)
                if product and quantity:
                    total += product.price * quantity

    # Return only the inner content for the #order-total div
    return HttpResponse(f"Total: ${total:.2f}")

def add_item_row(request):
    """Returns a single empty form row to be appended to the formset."""
    formset = OrderItemFormSet()
    form = formset.forms[-1] 
    return render(request, 'partials/item_row.html', {'form': form})

def order_list_partial(request):
    orders = Order.objects.all().order_by('-id')
    return render(request, 'partials/order_list.html', {'orders': orders})

def stock_list_partial(request):
    stock = Stock.objects.all().order_by('-id')
    return render(request, 'partials/stock_list.html', {'stock': stock})

def process_checkout(request):

    if request.method != "POST":
        return JsonResponse(
            {"status": "error", "message": "Invalid request method"}, status=405
        )

    try:
        cart = json.loads(request.body)
    except Exception:
        return JsonResponse(
            {"status": "error", "message": "Invalid JSON payload"}, status=400
        )

    is_valid, validation_message = validate_cart_stock(cart)
    if not is_valid:
        return JsonResponse(
            {
                "status": "error",
                "message": "Cannot complete order. Out of stock!",
                "missing_details": validation_message,
            },
            status=400,
        )

    customer_name = None
    if isinstance(cart, dict) and "items" in cart:

        customer_name = cart.get("customer_name")
        cart = cart["items"]

    try:
        with transaction.atomic():
            order = Order.objects.create(
                customer_name=customer_name, total_price=0.0 )

            total_price = Decimal(0)
            created_items = []

            for item in cart:
                item_type = item.get("type")
                product_id = item.get("id")
                qty = int(item.get("quantity", 0))

                if qty <= 0:
                    continue

                # Load the concrete product so we can call update_stock() on the correct model
                if item_type == "burger":
                    product = Burger.objects.select_related("recipe").get(id=product_id)
                elif item_type == "beverage":
                    product = Beverage.objects.select_related("stock").get(
                        id=product_id
                    )
                else:
                    continue

                line_total = (product.price) * qty
                total_price += line_total

                created_items.append(
                    OrderItem(order=order, product=product, quantity=qty)
                )

                # Subtract stock (ingredients for burgers, stock for beverages)
                product.update_stock(qty)

            OrderItem.objects.bulk_create(created_items)

            order.total_price = total_price
            order.save(update_fields=["total_price"])

        return JsonResponse(
            {
                "status": "success",
                "message": "Order processed and stock updated!",
                "order_id": order.id,
                "total_price": order.total_price,
            }
        )

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
    
