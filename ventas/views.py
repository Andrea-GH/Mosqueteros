# ventas/views.py
from django.shortcuts import render
from django.views.decorators.http import require_GET
from .models import Venta
from .utils import CurrencyConverter
from decimal import Decimal


@require_GET
def lista_ventas(request):
    ventas = Venta.objects.select_related(
        'cliente',
        'sucursal',
        'vendedor',
        'metodo_pago'
    ).prefetch_related('detalles').all()
    
    # Obtener moneda seleccionada (por defecto MXN)
    currency = request.GET.get('currency', 'MXN').upper()
    
    # Validar moneda
    if currency not in ['MXN', 'USD', 'EUR']:
        currency = 'MXN'
    
    # Procesar cada venta para convertir sus montos
    for venta in ventas:
        venta.subtotal_original = venta.subtotal
        venta.impuesto_original = venta.impuesto
        venta.total_original = venta.total
        
        if currency != 'MXN':
            venta.subtotal = CurrencyConverter.convert(venta.subtotal, 'MXN', currency)
            venta.impuesto = CurrencyConverter.convert(venta.impuesto, 'MXN', currency)
            venta.total = CurrencyConverter.convert(venta.total, 'MXN', currency)
        
        venta.moneda = currency
    
    # Calcular totales generales
    total_general_mxn = sum(v.total_original for v in ventas)
    total_general = CurrencyConverter.convert(total_general_mxn, 'MXN', currency)
    
    # Tasas de cambio para mostrar en el template (usando los atributos de la clase)
    context = {
        'ventas': ventas,
        'current_currency': currency,
        'total_general': total_general,
        'total_general_mxn': total_general_mxn,
        'exchange_rates': {
            'MXN_TO_USD': CurrencyConverter.MXN_TO_USD,
            'MXN_TO_EUR': CurrencyConverter.MXN_TO_EUR,
            'USD_TO_MXN': CurrencyConverter.USD_TO_MXN,
            'USD_TO_EUR': CurrencyConverter.USD_TO_EUR,
            'EUR_TO_MXN': CurrencyConverter.EUR_TO_MXN,
            'EUR_TO_USD': CurrencyConverter.EUR_TO_USD,
        }
    }
    
    return render(request, 'ventas/lista_ventas.html', context)