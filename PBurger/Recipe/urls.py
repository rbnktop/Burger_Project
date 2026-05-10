from django.urls import path
from . import views

app_name = "recipe"

urlpatterns = [

    path("Inventario/",
        views.list_recipe_view, 
        name="receita_inventario"
        ),

    path("Criar/",
        views.create_recipe_view, 
        name="receita_criar"
        ),
    path(
        "Editar/<int:recipe_id>",
        views.update_recipe_view,
        name="receita_editar",
    ),
    path(
        "Apagar/<int:recipe_id>",
        views.delete_recipe_view,
        name="receita_apagar",
    ),
]