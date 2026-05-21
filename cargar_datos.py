import pandas as pd
from ventas.models import Venta

# Carga el archivo Excel
df = pd.read_excel('tu_archivo_nuevo.xlsx') 

# Recorre cada fila e insértala en la base de datos
for index, fila in df.iterrows():
    Venta.objects.create(
        folio=fila['Folio'],      # Asegúrate que 'Folio' sea el nombre de la columna en Excel
        total=fila['Total'],      # Asegúrate que 'Total' sea el nombre de la columna en Excel
        # Agrega aquí los demás campos según tu modelo
    )

print("Migración completada exitosamente")
exit()