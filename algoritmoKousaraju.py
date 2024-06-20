import csv
from collections import defaultdict

def load_csv(filename):
    nodo_lista = defaultdict(list)
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            node = row[0]
            adjacency_list = row[1:] if len(row) > 1 else []
            nodo_lista[node] = adjacency_list
    return nodo_lista

def dfs(graph, node, visited, stack):
    visited.add(node)
    for neighbor in graph.get(node, []):
        if neighbor not in visited:
            dfs(graph, neighbor, visited, stack)
    stack.append(node)

def transpose_graph(graph):
    transposed = defaultdict(list)
    for node in graph:
        for neighbor in graph[node]:
            transposed[neighbor].append(node)
    return transposed

def kosaraju(graph):
    stack = []
    visited = set()
    for node in graph:
        if node not in visited:
            dfs(graph, node, visited, stack)
    transposed = transpose_graph(graph)
    visited.clear()
    sccs = []
    while stack:
        node = stack.pop()
        if node not in visited:
            scc_stack = []
            dfs(transposed, node, visited, scc_stack)
            sccs.append(scc_stack)
    return sccs

def run_kosaraju(csv_filename):
    nodo_lista = load_csv(csv_filename)
    sccs = kosaraju(nodo_lista)
    return nodo_lista, sccs

if __name__ == "__main__":
    csv_filename = 'prueba1.csv'  # Cambiar al archivo CSV deseado
    nodo_lista, sccs = run_kosaraju(csv_filename)
    print("Componentes Fuertemente Conexas (SCCs):", sccs)
