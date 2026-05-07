from django.urls import path
from . import views

app_name =  'stock'

urlpatterns = [
    path('Inventario/', views.list_stock_view, name="inventario"),
    path('Criar/', views.create_stock_item_view, name="criar"),
    path('Editar/<int:stock_id>', views.update_stock_item_view, name="editar"),
    path('Apagar/<int:stock_id>', views.delete_stock_item_view, name="apagar"),
    
    path('Receita/', views.list_recipe_view, name="receita"),
    path('Receita/Criar', views.create_recipe_view, name="receita_criar"),
    path('Receita/Editar/<int:stock_id>', views.update_stock_item_view, name="receita_editar"),
    path('Receita/Apagar/<int:stock_id>', views.delete_stock_item_view, name="receita_apagar"),
]