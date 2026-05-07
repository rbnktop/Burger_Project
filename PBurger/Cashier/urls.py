from django.urls import path
from .views import process_checkout

urlpatterns = [
    path("checkout/", process_checkout, name="process_checkout"),
]
