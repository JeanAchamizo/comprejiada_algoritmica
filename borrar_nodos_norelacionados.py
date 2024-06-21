import csv


# Inicializar un diccionario para almacenar nodos y sus listas de adyacencia
nodo_lista = {}

# Leer el archivo CSV
with open('top_5000_nodes.csv', 'r') as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        node = row[0]
        adjacency_list = row[1:] if len(row) > 1 else []  # Tomar todos los elementos después del primer elemento como la lista de adyacencia
        nodo_lista[node] = adjacency_list

# Imprimir el diccionario nodo_lista
# Obtener las claves del diccionario
claves = nodo_lista.keys()

# Iterar sobre cada clave y su lista de adyacencia
for nodo, lista_adyacencia in nodo_lista.items():
    # Filtrar la lista de adyacencia para eliminar los valores que no son claves en el diccionario
    #nodo_lista[nodo] = [valor for valor in lista_adyacencia if valor in claves]
    # Filtrar la lista de adyacencia para eliminar los valores que no son claves en el diccionario y ademas que las claves no esten en su propia lista de adyacencia
    nodo_lista[nodo] = [valor for valor in lista_adyacencia if valor in claves and valor != nodo]

# Escribir el diccionario actualizado en un archivo CSV
with open('top_5000_nodes.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for nodo, lista_adyacencia in nodo_lista.items():
        writer.writerow([nodo] + lista_adyacencia)

print("termine")
