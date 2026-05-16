from django.shortcuts import render
from django.http import HttpResponse
from django.db import transaction
from django.template.loader import render_to_string

from decimal import Decimal
from collections import defaultdict

from Inventory.models import Stock
from Menu.models import Product
from .models import Order, OrderItem

from .forms import OrderForm, OrderItemFormSet
from .services import check_order



def hub_view(request):
    products = Product.objects.all().order_by("-total_sold")
    initial_data = [{"product": p.id, "quantity": 0} for p in products]  # type: ignore

    formset_class = OrderItemFormSet
    
    # 2. Force extra to match your live product count on EVERY page load
    formset_class.extra = len(initial_data) #type:ignore

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
    """
    series of validations before commiting the order
    those include standard form validations and checking using check_order service,
    to see if the order is available for production based on the ingredients in stock. 
    """
    products = Product.objects.all().order_by("-total_sold")
    formset_class = OrderItemFormSet
    
    # 2. Force extra to match your live product count on EVERY page load
    formset_class.extra = len(initial_data) #type:ignore
    
    if request.method == "POST":
        form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            try:
                is_available, message = check_order(formset)
                if not is_available:
                    context = {
                        "status": False,
                        "status_message": message,
                        "products": products,
                        "form": form,
                        "formset": formset,
                    }
                    return render(request, "partials/order_update.html", context)
                
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
                    "status": True,
                    "form": empty_form,
                    "formset": empty_formset,
                    "new_order": order, 
                    "products": products,
                    "stock": Stock.objects.all().order_by("-updated_at"),
                }
                return render(request, "partials/order_update.html", context)

            except Exception as e:

                return HttpResponse(f"Error processing order: {e}", status=500)
            
        else:
            form_errors = []
            
            for field, error in form.errors.items():
                form_errors.append(f"Campo '{field}': {error.as_text()}")
            
            for err in formset.non_form_errors():
                form_errors.append(err)

            context = {
                "status": False,
                "status_message": form_errors, 
                "form": form,
                "formset": formset,
                "products": products,
            }
            return render(request, "partials/order_update.html", context)


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
        "status": False,
    }

    return render(request, "partials/order_update.html", context)


def calculate_order_total(request):
    """
    Calculates the total on-the-fly using only POST data.
    And calculate required ingredients for that order.
    """

    formset = OrderItemFormSet(request.POST)
    total = Decimal("0.00")
    required_ingredients = defaultdict(Decimal)
    errors = []

    if formset.is_valid():
        for form in formset:
            if not form.cleaned_data.get("DELETE"):
                product = form.cleaned_data.get("product")
                quantity = form.cleaned_data.get("quantity", 0)

                if product and quantity > 0:
                    total += product.price * quantity
                    

                    if hasattr(product, 'dish') and product.dish:
                        for recipe_item in product.dish.recipe_items.all():
                            stock_item = recipe_item.ingredient
                            if stock_item:
                                required_ingredients[stock_item] += Decimal(recipe_item.amount) * Decimal(quantity)
                    
                    elif hasattr(product, 'stock') and product.stock:
                        required_ingredients[product.stock] += Decimal(quantity)

        
        for stock_item, needed in required_ingredients.items():
            if stock_item.quantity < needed:
                diff = needed - Decimal(stock_item.quantity)
                errors.append(f"{stock_item.name}: falta {diff}{stock_item.unit}")

    oob_html = render_to_string("partials/status_update.html", {
        "missing": errors,
        "current_total": f"{total:.2f}"
    })

    return HttpResponse(f"{total:.2f}" + oob_html)


def order_list_partial(request):
    orders = Order.objects.all().order_by("-id")
    return render(request, "partials/order_list.html", {"orders": orders})


def stock_list_partial(request):
    stock = Stock.objects.all().order_by("-id")
    return render(request, "partials/stock_list.html", {"stock": stock})


