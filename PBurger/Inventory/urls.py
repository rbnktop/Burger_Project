from django.urls import path
from . import views

urlpatterns = [
    path('Criar/', views.create_stock_item_view, name="criar"),
    path('Lista/', views.list_stock_view, name="listar"),
    path('Atualizar/<int:stock_id>', views.update_stock_item_view, name="atualizar"),
    path('Apagar/<int:stock_id>', views.delete_stock_item_view, name="apagar"),

]