from django.urls import path
from .views import index, galeria, api, formulario, sobrenosotros, crear, articulos, eliminar, modificar, registrar

urlpatterns = [
    path('', index, name="index"),
    path('galeria/', galeria, name="galeria"),
    path('api/', api, name="api"),
    path('formulario/', formulario, name="formulario"),
    path('sobrenosotros/', sobrenosotros, name="sobrenosotros"),
    path('articulos/', articulos, name="articulos"),
    path('crear/', crear, name="crear"),
    path('eliminar/<id>', eliminar, name="eliminar"),
    path('modificar/<id>', modificar, name="modificar"),
    path('registrar/', registrar, name="registrar")
]