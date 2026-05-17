from django.urls import path
from . import views

app_name = "menu"

urlpatterns = [
    path("Produto/", views.list_product_view, name="inventario"),
    path("Produto/Criar", views.create_product_view, name="criar"),
    path(
        "Produto/Editar/<int:product_id>",
        views.update_product_view,
        name="editar",
    ),
    path(
        "Produto/Apagar/<int:product_id>",
        views.delete_product_view,
        name="apagar",
    ),
]
