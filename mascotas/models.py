from distutils.command.upload import upload
from django.db import models

# Create your models here.
class Categoria(models.Model):
    idCategoria = models.IntegerField(primary_key=True, verbose_name="Id de Categoria")
    nombreCategoria=models.CharField(max_length=50, blank=True, verbose_name="Nombre de categoria")

    def __str__(self):
        return self.nombreCategoria

class Producto(models.Model):
    codigo = models.CharField(primary_key=True, max_length=5, verbose_name="Codigo")
    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    descripcion = models.TextField(max_length=50, verbose_name="Descripcion")
    precio = models.IntegerField(verbose_name="Precio")
    categoria=models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name="Categoria")
    imagen = models.ImageField(upload_to="imagenes", null=True, blank=True, verbose_name="Imagen")

    def __str__(self):
        return self.codigo