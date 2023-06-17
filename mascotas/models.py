from distutils.command.upload import upload
from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class Producto(models.Model):
    codigo = models.CharField(primary_key=True, max_length=5, verbose_name="Codigo")
    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    descripcion = models.TextField(max_length=50, verbose_name="Descripcion")
    precio = models.IntegerField(verbose_name="Precio")
    imagen = models.ImageField(upload_to="imagenes", null=True, blank=True, verbose_name="Imagen")

    def __str__(self):
        return self.codigo