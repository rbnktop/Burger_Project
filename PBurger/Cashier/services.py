from Inventory.models import Stock, Dish, NonDish


def validate_cart_stock(cart_items):
    """
    Analyzes the entire cart to ensure we have enough stock.
    cart_items format: [{'id': 1, 'category': 'dish', 'quantity': 2}, ...]
    """

    total_stock_needed = {}

    for item in cart_items:
        product_id = item["id"]
        qty = item["quantity"]

        if item["category"] == "dish":
            dish = Dish.objects.get(id=product_id)

            for req in dish.recipe.ingredients.all():  # type: ignore
                ingredient_id = req.ingredient.pk
                amount_needed = req.amount * qty

                total_stock_needed[ingredient_id] = (
                    total_stock_needed.get(ingredient_id, 0) + amount_needed
                )

        elif item["category"] == "nondish":
            bev = NonDish.objects.get(id=product_id)
            ingredient_id = bev.stock.pk
            total_stock_needed[ingredient_id] = (
                total_stock_needed.get(ingredient_id, 0) + qty
            )

    missing_items = []

    for ingredient_id, needed_amount in total_stock_needed.items():
        actual_stock = Stock.objects.get(id=ingredient_id)

        if actual_stock.quantity < needed_amount:

            missing_items.append(
                f"Missing {actual_stock.name}: Need {needed_amount}{actual_stock.unit}, "
                f"but only have {actual_stock.quantity}{actual_stock.unit}."
            )

    if missing_items:
        return False, missing_items

    return True, "All items in stock!"
