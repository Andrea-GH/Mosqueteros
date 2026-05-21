# cargar_completo.py
import os
import django
import pandas as pd
from decimal import Decimal

# Configurar el entorno de Django apuntando al núcleo correcto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from ventas.models import Venta, DetalleVenta
from catalogos.models import Cliente, Vendedor, MetodoPago, Sucursal, Producto, Categoria
from django.utils import timezone

def importar_datos():
    print("Iniciando lectura del Excel...")
    try:
        df = pd.read_excel('Dashboard2021.xlsx')
    except Exception as e:
        print(f"No se pudo leer el archivo Excel: {e}")
        return

    print("Limpiando tablas de la base de datos para asegurar carga limpia...")
    DetalleVenta.objects.all().delete()
    Venta.objects.all().delete()

    print(f"Filas detectadas para procesar: {len(df)}")
    ventas_creadas = 0
    detalles_creados = 0

    for index, fila in df.iterrows():
        try:
            # 1. Crear u obtener registros de catálogos básicos
            sucursal_obj, _ = Sucursal.objects.get_or_create(nombre=str(fila['Ciudad']))
            
            vendedor_obj, _ = Vendedor.objects.get_or_create(
                nombre=str(fila['Vendedor']),
                defaults={'sucursal': sucursal_obj}
            )
            
            cliente_obj, _ = Cliente.objects.get_or_create(nombre=str(fila['Cliente']))
            metodo_obj, _ = MetodoPago.objects.get_or_create(nombre=str(fila['Forma de pago']))
            categoria_obj, _ = Categoria.objects.get_or_create(nombre=str(fila['Categoría']))
            
            # 2. Desglose de montos para cumplir con las restricciones de Venta y Detalle
            total_fila = float(fila['Ventas'])
            subtotal_calculado = round(total_fila / 1.16, 2)
            impuesto_calculado = round(total_fila - subtotal_calculado, 2)
            
            precio_unitario = Decimal(str(total_fila))
            cantidad_val = int(fila.get('Cantidad', 1))
            
            # Generar un código único simple basado en el nombre del producto para evitar el UNIQUE constraint
            nombre_prod = str(fila['Producto'])
            codigo_unico = "".join([c for c in nombre_prod if c.isalnum()]).upper()[:10] + f"_{index}"
            
            # 3. Crear o buscar producto (agregando el código único en defaults)
            producto_obj, _ = Producto.objects.get_or_create(
                nombre=nombre_prod,
                defaults={
                    'categoria': categoria_obj,
                    'precio': precio_unitario,
                    'codigo': codigo_unico  # <--- CORRECCIÓN: Evita el error UNIQUE constraint
                }
            )
            
            # 4. Crear o buscar Cabecera de la Venta
            fecha_val = fila['Fecha'] if pd.notnull(fila['Fecha']) else timezone.now()
            venta_obj, creada = Venta.objects.get_or_create(
                folio=str(fila['Documento']),
                defaults={
                    'subtotal': subtotal_calculado,
                    'impuesto': impuesto_calculado,
                    'total': total_fila,
                    'cliente': cliente_obj,
                    'vendedor': vendedor_obj,
                    'metodo_pago': metodo_obj,
                    'sucursal': sucursal_obj,
                    'fecha': fecha_val
                }
            )
            
            if not creada:
                venta_obj.subtotal += subtotal_calculado
                venta_obj.impuesto += impuesto_calculado
                venta_obj.total += total_fila
                venta_obj.save()
            else:
                ventas_creadas += 1
            
            # 5. Crear el detalle incluyendo el subtotal obligatorio del modelo
            DetalleVenta.objects.create(
                venta=venta_obj,
                producto=producto_obj,
                cantidad=cantidad_val,
                precio_unitario=precio_unitario,
                subtotal=subtotal_calculado  # <--- CORRECCIÓN: Evita el error NOT NULL constraint
            )
            detalles_creados += 1
            
        except Exception as error_fila:
            # Ahora sí imprimirá si algo llega a fallar de forma aislada
            print(f"Error en fila {index} (Documento: {fila.get('Documento')}): {error_fila}")

    print("\n--- ¡MIGRACIÓN COMPLETADA CON ÉXITO! ---")
    print(f"Total Ventas únicas en base: {Venta.objects.count()}")
    print(f"Total Detalles en base: {DetalleVenta.objects.count()}")

if __name__ == '__main__':
    importar_datos()