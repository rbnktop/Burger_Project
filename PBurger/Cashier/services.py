from Inventory.models import Stock, Burger, Beverage


def validate_cart_stock(cart_items):
    """
    Analyzes the entire cart to ensure we have enough stock.
    cart_items format: [{'id': 1, 'type': 'burger', 'quantity': 2}, ...]
    """

    total_stock_needed = {}

    for item in cart_items:
        product_id = item["id"]
        qty = item["quantity"]

        if item["type"] == "burger":
            burger = Burger.objects.get(id=product_id)
            # Loop through the recipe requirements
            for req in burger.recipe.ingredients.all():
                stock_id = req.ingredient.pk
                amount_needed = req.amount * qty

                total_stock_needed[stock_id] = (
                    total_stock_needed.get(stock_id, 0) + amount_needed
                )

        elif item["type"] == "beverage":
            bev = Beverage.objects.get(id=product_id)
            stock_id = bev.stock.pk
            total_stock_needed[stock_id] = total_stock_needed.get(stock_id, 0) + qty

    missing_items = []

    for stock_id, needed_amount in total_stock_needed.items():
        actual_stock = Stock.objects.get(id=stock_id)

        if actual_stock.quantity < needed_amount:

            missing_items.append(
                f"Missing {actual_stock.name}: Need {needed_amount}{actual_stock.unit}, "
                f"but only have {actual_stock.quantity}{actual_stock.unit}."
            )

    if missing_items:
        return False, missing_items

    return True, "All items in stock!"
