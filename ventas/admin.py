from django.contrib import admin
from .models import Venta, DetalleVenta


class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'folio', 'fecha', 'cliente', 'sucursal',
        'vendedor', 'metodo_pago', 'subtotal', 'impuesto', 'total'
    )
    search_fields = ('folio', 'cliente__nombre', 'vendedor__nombre')
    list_filter = ('fecha', 'sucursal', 'metodo_pago', 'vendedor')
    inlines = [DetalleVentaInline]


@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'venta', 'producto', 'cantidad', 'precio_unitario', 'subtotal')
    search_fields = ('venta__folio', 'producto__nombre')
    list_filter = ('producto',)
