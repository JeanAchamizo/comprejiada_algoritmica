import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import csv
import os

# Inicializar un diccionario para almacenar nodos y sus listas de adyacencia
nodo_lista = {}

# Leer el archivo CSV
with open('prueba_limpio.csv', 'r') as file:
#with open('datos_1_limpio.csv', 'r') as file:
#with open('datos_1.csv', 'r') as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        node = row[0]
        adjacency_list = row[1:] if len(row) > 1 else []  # Tomar todos los elementos después del primer elemento como la lista de adyacencia
        nodo_lista[node] = adjacency_list


# Implementación del algoritmo de Kosaraju
def dfs(graph, node, visited, stack):
    visited.add(node)
    for neighbor in graph.get(node, []):
        if neighbor not in visited:
            dfs(graph, neighbor, visited, stack)
    stack.append(node)

def transpose_graph(graph):
    transposed = {}
    for node in graph:
        for neighbor in graph[node]:
            if neighbor not in transposed:
                transposed[neighbor] = []
            transposed[neighbor].append(node)
    return transposed

def kosaraju(graph):
    stack = []
    visited = set()

    # Paso 1: Realizar DFS y almacenar el orden de finalización
    for node in graph:
        if node not in visited:
            dfs(graph, node, visited, stack)

    # Paso 2: Transponer el grafo
    transposed = transpose_graph(graph)

    # Paso 3: Realizar DFS en el grafo transpuesto en el orden de los tiempos de finalización
    visited.clear()
    sccs = []
    while stack:
        node = stack.pop()
        if node not in visited:
            scc_stack = []
            dfs(transposed, node, visited, scc_stack)
            sccs.append(scc_stack)

    return sccs

# Ejecutar el algoritmo de Kosaraju en nodo_lista
sccs = kosaraju(nodo_lista)

print("Componentes Fuertemente Conexas (SCCs):", sccs)

# Crear un objeto Network para visualización
#net = Network()
# Crear un objeto Network para visualización como grafo dirigido
net = Network(directed=True, height='100%', width='100%')
# Ajustar la configuración de física del grafo
net.barnes_hut()

net1 = Network(directed=True,height='100%', width='100%')
net1.barnes_hut()
# Agregar nodos al gráfico original y al gráfico de componentes fuertemente conexas
for nodo, seguidores in nodo_lista.items():
    net.add_node(nodo)
    net1.add_node(nodo)
    for seguidor in seguidores:
        net.add_node(seguidor)
        net.add_edge(nodo,seguidor)


padres = list(nodo_lista.keys())
# tomar el primer nodo de cada scc y conectarlo con los nodos de la scc y el ultimo conectarlo con el primero 

for scc in sccs:
    if len(scc) > 0:
        padre = scc[0]
        for hijo in scc[1:]:
            net1.add_edge(padre,hijo)

## Visualizar el gráfico ##

# Nombre de la carpeta donde se guardarán los archivos HTML
folder_name = 'template'

# Verificar si la carpeta existe. Si no, crearla.
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Guardar los archivos HTML en la carpeta especificada
net.show(os.path.join(folder_name, 'grafo_original.html'))
net1.show(os.path.join(folder_name, 'grafo_scc.html'))
