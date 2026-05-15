from decimal import Decimal
from django.shortcuts import render
from django.http import HttpResponse
from django.db import transaction

from Inventory.models import Stock
from Menu.models import Product

from .models import Order, OrderItem
from .forms import OrderForm, OrderItemFormSet



def hub_view(request):
    products = list(Product.objects.all().order_by("-total_sold"))
    initial_data = [{"product": p.id, "quantity": 0} for p in products]  # type: ignore

    form = OrderForm()
    formset = OrderItemFormSet(initial=initial_data, queryset=OrderItem.objects.none())

    return render(
        request,
        "hub.html",
        {
            "form": form,
            "formset": formset,
            "products": products,
        },
    )




def process_order(request):
    # Fetch products for the 'Initial' grid layout
    products = list(Product.objects.all().order_by("-total_sold"))
    
    if request.method == "POST":
        form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    order = form.save()
                    
                    instances = formset.save(commit=False)
                    for instance in instances:
                        if instance.quantity > 0:
                            instance.order = order
                            instance.save() 

                    order.update_price()


                initial_data = [{"product": p.id, "quantity": 0} for p in products] #type:ignore
                empty_form = OrderForm()
                empty_formset = OrderItemFormSet(
                    initial=initial_data, 
                    queryset=OrderItem.objects.none()
                )

                context = {
                    "form": empty_form,
                    "formset": empty_formset,
                    "products": products,
                    "new_order": order, 
                    "stock": Stock.objects.all().order_by("-updated_at"),
                    "status": True,
                }
                return render(request, "partials/order_update.html", context)

            except Exception as e:

                return HttpResponse(f"Error processing order: {e}", status=500)


    else:
        initial_data = [{"product": p.pk, "quantity": 0} for p in products]
        form = OrderForm()
        formset = OrderItemFormSet(
            initial=initial_data, 
            queryset=OrderItem.objects.none()
        )

    context = {
        "form": form,
        "formset": formset,
        "products": products,
        "new_order": Order.objects.all().order_by("-id")[:25],
        "stock": Stock.objects.all().order_by("-updated_at"),
        "status": False,
    }

    return render(request, "partials/order_update.html", context)


def calculate_order_total(request):
    """
    Calculates the total on-the-fly using only POST data.
    Does not require the Order to exist in the DB yet.
    """

    formset = OrderItemFormSet(request.POST)
    total = Decimal("0.00")

    # Force Django to populate cleaned_data, but ignore the ForeignKey errors
    for form in formset:
        form.is_valid() 
        if not form.cleaned_data.get("DELETE"):
            product = form.cleaned_data.get("product")
            quantity = form.cleaned_data.get("quantity", 0)
            if product and quantity:
                total += product.price * quantity

 
    return HttpResponse(f"{total:.2f}")


def order_list_partial(request):
    orders = Order.objects.all().order_by("-id")
    return render(request, "partials/order_list.html", {"orders": orders})


def stock_list_partial(request):
    stock = Stock.objects.all().order_by("-id")
    return render(request, "partials/stock_list.html", {"stock": stock})


