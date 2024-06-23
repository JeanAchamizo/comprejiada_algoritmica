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

 
twitter_adj_list = dataframe_to_adjacency_list(twitter, "start_node", "end_node") #tamaño de la lista de adyacencia l -> 70097
# que imprima el key numero mas grande

nodomayo = max(twitter_adj_list, key=int)
nodomenor = min(twitter_adj_list, key=int)
print(nodomayo)
print(nodomenor)



print("termine")
