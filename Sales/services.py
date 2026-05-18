from collections import defaultdict
from Inventory.models import Stock
from Menu.models import Dish, NonDish


def check_order(formset):
    """
    Returns (is_available, error_list)
    """

    total_qty = sum(
        f.cleaned_data.get('quantity', 0) 
        for f in formset 
        if not f.cleaned_data.get('DELETE', False)
    )
    
    if total_qty <= 0:
        return False, ["O pedido não pode estar vazio!"]
    
    requirements = defaultdict(float)
    errors = []

    for item_form in formset:
        qty = item_form.cleaned_data.get("quantity", 0)
        product = item_form.cleaned_data.get("product")
        
        if qty > 0 and product:
            if hasattr(product, 'dish') and product.dish:
                for recipe_item in product.dish.recipe_items.all():
                    ing = recipe_item.ingredient
                    requirements[ing.id] += float(recipe_item.amount * qty)
            elif hasattr(product, 'stock') and product.stock:
                requirements[product.stock.id] += float(qty)


    for stock_id, needed in requirements.items():
        stock_item = Stock.objects.get(id=stock_id)
        if stock_item.quantity < needed:
            diff = needed - float(stock_item.quantity)
            errors.append(f"{stock_item.name}: falta {diff:.1f} {stock_item.unit_display}")

    return len(errors) == 0, errors


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


