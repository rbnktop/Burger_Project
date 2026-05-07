from django.http import JsonResponse
from django.db import transaction
from Inventory.models import Beverage, Burger
from .services import validate_cart_stock

import json


def process_checkout(request):
    if request.method == "POST":

        cart_items = json.loads(request.body)
        is_valid, validation_message = validate_cart_stock(cart_items)

        if not is_valid:

            return JsonResponse(
                {
                    "status": "error",
                    "message": "Cannot complete order. Out of stock!",
                    "missing_details": validation_message,
                },
                status=400,
            )

        try:
            with transaction.atomic():
                # loop through and use the update_stock() / subtract_stock()

                for item in cart_items:
                    if item["type"] == "burger":
                        product = Burger.objects.get(id=item["id"])
                        product.update_stock(item["quantity"])
                    elif item["type"] == "beverage":
                        product = Beverage.objects.get(id=item["id"])
                        product.update_stock(item["quantity"])

                # (You would also save the actual 'Order' and 'OrderItem' rows to the DB here)

            return JsonResponse(
                {"status": "success", "message": "Order processed and stock updated!"}
            )

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse(
        {"status": "error", "message": "Invalid request method"}, status=405
    )
