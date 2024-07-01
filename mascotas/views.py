from django.shortcuts import render, redirect
from .models import *
from .forms import ProductoForm, RegistroUserForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from mascotas.compra import Carrito
from django.core.paginator import Paginator

# Create your views here.

def index(request):
    productos = Producto.objects.all()
    paginator = Paginator(productos, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'productos': page_obj}
    return render(request, 'index.html', context)

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
            producto_form = productoform.save(commit=False)
            
            if 'imagen' in request.FILES:
                imagen = request.FILES['imagen']
                
                if producto.imagen:
                    default_storage.delete(producto.imagen.path)
                
                producto_form.imagen = imagen
            
            producto_form.save()
            return redirect('articulos')
    return render(request, 'modificar.html', datos)

@login_required
def crear(request):
    if request.method=='POST':
        productoform = ProductoForm(request.POST, request.FILES)
        if productoform.is_valid():
            productoform.save()
            return redirect('articulos')
    else:
        productoform=ProductoForm()
    return render(request, 'crear.html',{'productoform': productoform})


def registrar(request):
    data = {
        'form' : RegistroUserForm()
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

@login_required
def agregar_producto(request,id):
    carrito_compra= Carrito(request)
    producto = Producto.objects.get(codigo=id)
    carrito_compra.agregar(producto=producto)
    return redirect('galeria')

@login_required
def eliminar_producto(request, id):
    carrito_compra= Carrito(request)
    producto = Producto.objects.get(codigo=id)
    carrito_compra.eliminar(producto=producto)
    return redirect('galeria')

@login_required
def restar_producto(request, id):
    carrito_compra= Carrito(request)
    producto = Producto.objects.get(codigo=id)
    carrito_compra.restar(producto=producto)
    return redirect('galeria')

@login_required
def limpiar_carrito(request):
    carrito_compra= Carrito(request)
    carrito_compra.limpiar()
    return redirect('galeria')

from collections import defaultdict

from collections import defaultdict

@login_required
def generarBoleta(request):
    precio_total = 0
    envio = 3990
    impuesto_producto = 5990

    subtotales = defaultdict(int)

    for key, value in request.session['carrito'].items():
        cantidad = int(value['cantidad'])
        precio = int(value['precio'])

        subtotal = cantidad * precio

        if cantidad >= 4:
            subtotal += impuesto_producto

        subtotales[value['producto_id']] += subtotal

    precio_total = sum(subtotales.values())
    precio_total += envio

    usuario_actual = request.user

    boleta = Boleta(total=precio_total, usuario=usuario_actual)
    boleta.save()

    productos = []
    for key, value in request.session['carrito'].items():
        producto = Producto.objects.get(codigo=value['producto_id'])
        cant = value['cantidad']
        subtotal = subtotales[value['producto_id']]
        detalle = detalle_boleta(id_boleta=boleta, id_producto=producto, cantidad=cant, subtotal=subtotal)
        detalle.save()
        productos.append(detalle)

        producto.stock -= cant
        producto.save()

    datos = {
        'productos': productos,
        'fecha': boleta.fechaCompra,
        'total': boleta.total,
        'usuario': boleta.usuario
    }
    request.session['boleta'] = boleta.id_boleta
    carrito = Carrito(request)
    carrito.limpiar()
    return render(request, 'detallecarrito.html', datos)
