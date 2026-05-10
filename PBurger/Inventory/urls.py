from django.urls import path
from . import views

app_name = "stock"

urlpatterns = [
    path("Inventario/", views.list_stock_view, name="inventario"),
    path("Inventario/Criar/", views.create_stock_item_view, name="criar"),
    path(
        "Inventario/Editar/<int:stock_id>", views.update_stock_item_view, name="editar"
    ),
    path(
        "Inventario/Apagar/<int:stock_id>", views.delete_stock_item_view, name="apagar"
    ),



    path("Receita/", views.list_recipe_view, name="receita_inventario"),
    path("Receita/Criar", views.create_recipe_view, name="receita_criar"),
    path(
        "Receita/Editar/<int:recipe_id>",
        views.update_recipe_view,
        name="receita_editar",
    ),
    path(
        "Receita/Apagar/<int:recipe_id>",
        views.delete_recipe_view,
        name="receita_apagar",
    ),



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
