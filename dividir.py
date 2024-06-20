
import csv

# Nombre del archivo CSV original
archivo_original = "top_5000_nodes.csv"

# Nombres de los archivos CSV resultantes
archivo_1 = "datos_1.csv"
archivo_2 = "datos_2.csv"

# Fila en la que se dividirá el archivo
fila_division = 200

# Listas para almacenar las filas divididas
conjunto_1 = []
conjunto_2 = []

# Leer el archivo CSV original y dividir los datos
with open(archivo_original, 'r', newline='') as file:
    reader = csv.reader(file)
    for i, row in enumerate(reader):
        if i < fila_division:
            conjunto_1.append(row)
        else:
            conjunto_2.append(row)

# Escribir los conjuntos divididos en archivos CSV separados
with open(archivo_1, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(conjunto_1)

with open(archivo_2, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(conjunto_2)

print("Archivos CSV divididos correctamente.")

