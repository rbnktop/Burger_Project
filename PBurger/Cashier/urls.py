from django.urls import path
from .views import process_checkout

app_name='cashier'

urlpatterns = [
    path("checkout/", process_checkout, name="checkout"),
]
