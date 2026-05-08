from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("Greeting.urls"), name="greeting"),
    path("Caixa/", include("Cashier.urls")),
    path("Stock/", include("Inventory.urls")),
]
