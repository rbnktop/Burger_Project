from collections import defaultdict
from Inventory.models import Stock

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
            # Check if it's a Dish (has a recipe) or a Non-Dish (direct stock)
            if hasattr(product, 'dish') and product.dish:
                # Calculate ingredients for the dish
                for recipe_item in product.dish.recipe_items.all():
                    ing = recipe_item.ingredient
                    requirements[ing.id] += float(recipe_item.amount * qty)
            elif hasattr(product, 'stock') and product.stock:
                # Direct item (like a Soda)
                requirements[product.stock.id] += float(qty)

    # Compare requirements against actual DB stock
    for stock_id, needed in requirements.items():
        stock_item = Stock.objects.get(id=stock_id)
        if stock_item.quantity < needed:
            diff = needed - float(stock_item.quantity)
            errors.append(f"{stock_item.name}: falta {diff:.1f} {stock_item.unit_display}")

    return len(errors) == 0, errors