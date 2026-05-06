from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include('Greeting.urls')),
    path('cashier/', include('Cashier.urls')),
    path('inventory/', include('Inventory.urls')),
]
