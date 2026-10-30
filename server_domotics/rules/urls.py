from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.rules, name="reglas"),
    path("crear/", views.add_rule, name="regla_crear"),
    path("<int:id>/", views.edit_rule, name="regla_editar"),
    path("<int:id>/eliminar/", views.delete_rule, name="regla_eliminar")
]