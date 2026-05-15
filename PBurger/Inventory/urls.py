from django.urls import path
from . import views

app_name = "stock"

urlpatterns = [
    path("Estoque/", views.list_stock_view, name="inventario"),
    path("Estoque/Criar/", views.create_stock_item_view, name="criar"),
    path("Estoque/Editar/<int:stock_id>", views.update_stock_item_view, name="editar"),
    path("Estoque/Apagar/<int:stock_id>", views.delete_stock_item_view, name="apagar"),
    path("Produto/", views.list_product_view, name="produto_inventario"),
    path("Produto/Criar", views.create_product_view, name="produto_criar"),
    path(
        "Produto/Editar/<int:product_id>",
        views.update_product_view,
        name="produto_editar",
    ),
    path(
        "Produto/Apagar/<int:product_id>",
        views.delete_product_view,
        name="produto_apagar",
    ),
]
