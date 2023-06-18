from django.shortcuts import render, redirect
from .models import *
from .forms import ProductoForm, RegistroUserForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage

# Create your views here.

def index(request):
    return render(request, 'index.html')

def galeria(request):
    articulos = Producto.objects.all()
    datos={
        'articulos': articulos
    }
    return render(request,'galeria.html',datos)

def api(request):
    return render(request, 'api.html')

def formulario(request):
    return render(request, 'formulario.html')

def sobrenosotros(request):
    return render(request, 'sobrenosotros.html')

def articulos(request):
    productos = Producto.objects.raw('Select * from mascotas_producto')
    datos ={'articulos':productos}
    return render(request, 'articulos.html', datos)

@login_required
def eliminar(request, id):
    productoEliminado=Producto.objects.get(codigo=id)  #obtenemos un objeto por su pk
    productoEliminado.delete()
    return redirect('articulos')

@login_required
def modificar(request, id):
    producto = Producto.objects.get(codigo=id)
    datos = {
        'form': ProductoForm(instance=producto)
    }
    if request.method == 'POST':
        productoform = ProductoForm(data=request.POST, files=request.FILES, instance=producto)
        if productoform.is_valid():
            # Guardar el formulario sin guardar la instancia del producto aún
            producto_form = productoform.save(commit=False)
            
            # Verificar si se proporcionó una nueva imagen
            if 'imagen' in request.FILES:
                imagen = request.FILES['imagen']
                
                # Eliminar la imagen anterior si existe
                if producto.imagen:
                    default_storage.delete(producto.imagen.path)
                
                # Guardar la nueva imagen
                producto_form.imagen = imagen
            
            # Guardar finalmente la instancia del producto
            producto_form.save()
            return redirect('articulos')
    return render(request, 'modificar.html', datos)

'''
def modificar(request, id):
    producto = Producto.objects.get(codigo=id)
    datos = {
        'form': ProductoForm(instance=producto)
    }
    if request.method == 'POST':
        productoform = ProductoForm(data=request.POST, instance=producto)
        if productoform.is_valid():  # Agregamos los paréntesis después de is_valid
            productoform.save()
            return redirect('articulos')
    return render(request, 'modificar.html', datos)
'''

@login_required
def crear(request):
    if request.method=='POST':
        productoform = ProductoForm(request.POST, request.FILES)
        if productoform.is_valid():
            productoform.save()     #similar al insert en función
            return redirect('articulos') #aqui va la página de administración de los productos
    else:
        productoform=ProductoForm()
    return render(request, 'crear.html',{'productoform': productoform}) #aqui debo poner la página para crear un nuevo producto

#método que permite registrar un usuario
def registrar(request):
    data = {
        'form' : RegistroUserForm()         #creamos un objeto de tipo forms para user
    }
    if request.method=="POST":
        formulario = RegistroUserForm(data = request.POST)  
        if formulario.is_valid():
            formulario.save()
            user= authenticate(username=formulario.cleaned_data["username"],
                  password=formulario.cleaned_data["password1"])
            login(request,user)   
            return redirect('index')
        data["form"] = formulario
    return render(request, 'registration/registro.html', data)