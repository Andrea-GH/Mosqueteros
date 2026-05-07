# ventas/urls.py
from django.urls import path
from .views import lista_ventas

urlpatterns = [
    path('', lista_ventas, name='lista_ventas'),
    # También podemos agregar un endpoint para obtener tasas actualizadas vía AJAX
    path('conversor/', lista_ventas, name='lista_ventas_conversor'),
]