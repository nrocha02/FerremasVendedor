from django.urls import path
from .views import index, galeria

urlpatterns = [
    path('', index, name="index"),
    path('galeria/', galeria, name="galeria"),
]