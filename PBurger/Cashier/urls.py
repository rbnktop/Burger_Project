from django.urls import path
from .views import (
    # process_checkout,
    hub_view,
    calculate_order_total,
    order_list_partial,
    stock_list_partial,
    process_order,
)

app_name = "cashier"

urlpatterns = [
    path("", hub_view, name="hub"),
    path("calculate-total/", calculate_order_total, name="calculate-total"),
    # path("checkout/", process_checkout, name="checkout"),
    path("order_list/", order_list_partial, name="order-list"),
    path("stock_list/", stock_list_partial, name="stock-list"),
    path("process_order/", process_order, name="process-order"),
]
