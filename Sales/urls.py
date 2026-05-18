from django.urls import path
from .views import (

    hub_view,
    calculate_order_total,
    order_list_partial,
    stock_list_partial,
    process_order,
)

app_name = "sales"

urlpatterns = [
    path("", hub_view, name="hub"),
    
    path("process_order/", process_order, name="process-order"),
    path("calculate-total/", calculate_order_total, name="calculate-total"),
    path("order_list/", order_list_partial, name="order-list"),
    path("stock_list/", stock_list_partial, name="stock-list"),
]
