from django.contrib import admin
from .models import Categoria, Sucursal, MetodoPago, Cliente, Vendedor, Producto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'activo')
    search_fields = ('nombre',)
    list_filter = ('activo',)


@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'ciudad', 'estado', 'pais', 'activo')
    search_fields = ('nombre', 'ciudad', 'estado', 'pais')
    list_filter = ('activo', 'estado', 'pais')


@admin.register(MetodoPago)
class MetodoPagoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'activo')
    search_fields = ('nombre',)
    list_filter = ('activo',)


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'telefono', 'correo', 'ciudad', 'estado', 'pais', 'activo')
    search_fields = ('nombre', 'correo', 'telefono')
    list_filter = ('activo', 'estado', 'pais')


@admin.register(Vendedor)
class VendedorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'correo', 'telefono', 'sucursal', 'activo')
    search_fields = ('nombre', 'correo', 'telefono')
    list_filter = ('activo', 'sucursal')


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo', 'nombre', 'categoria', 'precio', 'stock', 'activo')
    search_fields = ('codigo', 'nombre')
    list_filter = ('activo', 'categoria')

