from django.urls import path
from .views import process_checkout, hub_view

app_name='cashier'

urlpatterns = [
    path("hub/", hub_view, name="hub"),
    
    path("checkout/", process_checkout, name="checkout"),
]
