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
            order = Order.objects.create(customer_name=customer_name, total_price=0.0)

            total_price = Decimal(0)
            created_items = []

            for item in cart:
                item_type = item.get("type")
                product_id = item.get("id")
                qty = int(item.get("quantity", 0))

                if qty <= 0:
                    continue

                # Load the concrete product so we can call update_stock() on the correct model
                if item_type == "dish":
                    product = Dish.objects.select_related("recipe").get(id=product_id)
                elif item_type == "other":
                    product = NonDish.objects.select_related("stock").get(
                        id=product_id
                    )
                else:
                    continue

                line_total = (product.price) * qty
                total_price += line_total

                created_items.append(
                    OrderItem(order=order, product=product, quantity=qty)
                )

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
