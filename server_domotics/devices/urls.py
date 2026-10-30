from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.devices, name="dispositivos"),
    path("crear/", views.add_device, name="dispositivo_crear"),
    path("<int:id>/", views.edit_device, name="dispositivo_editar"),
    path("<int:id>/eliminar/", views.delete_device, name="dispositivo_eliminar"),
    path("<int:id>/consultar/", views.consult_device, name="dispositivo_consultar")
]