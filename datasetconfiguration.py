import pandas as pd
import time

import matplotlib.pyplot as plt
import seaborn as sns
import csv


# graph
import networkx as nx
from pyvis.network import Network
from random import randint

twitter = pd.read_csv(
    "twitter_combined.txt.gz",
    compression="gzip",
    sep=" ",
    names=["start_node", "end_node"],
)
twitter

def dataframe_to_adjacency_list(dataframe, start_col, end_col):
    adjacency_list = {}
    for index, row in dataframe.iterrows():
        start_node = row[start_col]
        end_node = row[end_col]
        
        # Agregar el nodo de inicio si no está en la lista de adyacencia
        if start_node not in adjacency_list:
            adjacency_list[start_node] = []
        
        # Agregar el nodo final a la lista de adyacencia del nodo de inicio
        adjacency_list[start_node].append(end_node)
        
    return adjacency_list


twitter_adj_list = dataframe_to_adjacency_list(twitter, "start_node", "end_node")

def reduce_to_top_nodes(adjacency_list, top_n=5000):
    # Ordenar los nodos por el tamaño de sus listas de adyacencia de forma descendente -> resverse=False
    sorted_nodes = sorted(adjacency_list.items(), key=lambda x: len(x[1]), reverse=False)
    
    # Tomar los primeros top_n nodos
    top_nodes = sorted_nodes[10000:20000]
    
    # Crear un nuevo diccionario con los nodos seleccionados
    reduced_adj_list = dict(top_nodes)
    
    return reduced_adj_list

def save_adjacency_list_to_csv(adjacency_list, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for node, neighbors in adjacency_list.items():
            writer.writerow([node] + neighbors)

# Reducir a los 5000 nodos principales
top_5000_adj_list = reduce_to_top_nodes(twitter_adj_list, top_n=5000)

# Guardar los nodos principales en un archivo CSV
save_adjacency_list_to_csv(top_5000_adj_list, 'top_5000_nodes.csv')


