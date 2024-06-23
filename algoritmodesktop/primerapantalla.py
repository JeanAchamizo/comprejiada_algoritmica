import sys
import csv
from collections import defaultdict
import networkx as nx
from pyvis.network import Network
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt
import os

class GraphApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Grafo de los datos del archivo')
        self.resize(1200, 600)
        self.setStyleSheet('background-color: #333; color: white;')
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(10, 10, 10, 10)
        mainLayout.setSpacing(0)

        buttonsLayout = QHBoxLayout()
        buttonsLayout.setSpacing(0)
        self.label = QLabel('Sube tu archivo:')
        buttonsLayout.addWidget(self.label)
        self.uploadButton = QPushButton('Enviar archivo')
        self.uploadButton.clicked.connect(self.loadCSV)
        buttonsLayout.addWidget(self.uploadButton)
        self.sccButton = QPushButton('Encontrar componentes fuertemente conexos')
        self.sccButton.clicked.connect(self.findSCCs)
        buttonsLayout.addWidget(self.sccButton)
        self.unionFindButton = QPushButton('Encontrar componentes conectados')
        self.unionFindButton.clicked.connect(self.findConnectedComponents)
        buttonsLayout.addWidget(self.unionFindButton)
        mainLayout.addLayout(buttonsLayout)

        graphsLayout = QHBoxLayout()
        graphsLayout.setSpacing(0)
        graphsLayout.setContentsMargins(0, 0, 0, 0)

        originalGraphLayout = QVBoxLayout()
        originalGraphLayout.setSpacing(0)
        originalGraphLayout.setContentsMargins(0, 0, 5, 0)
        self.graphLabel = QLabel('Grafo de los datos del archivo:')
        self.graphLabel.setFixedSize(600, 23)
        originalGraphLayout.addWidget(self.graphLabel)
        self.webViewOriginal = QWebEngineView()
        originalGraphLayout.addWidget(self.webViewOriginal)
        graphsLayout.addLayout(originalGraphLayout)
        
        sccGraphLayout = QVBoxLayout()
        sccGraphLayout.setSpacing(0)
        sccGraphLayout.setContentsMargins(0, 0, 0, 0)
        self.sccGraphLabel = QLabel('Grafo de los componentes fuertemente conexos:')
        self.sccGraphLabel.setFixedSize(600, 23)
        sccGraphLayout.addWidget(self.sccGraphLabel)
        self.webViewSCC = QWebEngineView()
        sccGraphLayout.addWidget(self.webViewSCC)
        graphsLayout.addLayout(sccGraphLayout)
        
        connectedComponentsLayout = QVBoxLayout()
        connectedComponentsLayout.setSpacing(0)
        connectedComponentsLayout.setContentsMargins(0, 0, 0, 0)
        self.connectedComponentsLabel = QLabel('Grafo de los componentes conectados:')
        self.connectedComponentsLabel.setFixedSize(600, 23)
        connectedComponentsLayout.addWidget(self.connectedComponentsLabel)
        self.webViewConnectedComponents = QWebEngineView()
        connectedComponentsLayout.addWidget(self.webViewConnectedComponents)
        graphsLayout.addLayout(connectedComponentsLayout)
        
        mainLayout.addLayout(graphsLayout)
        
        self.setLayout(mainLayout)
        
    def loadCSV(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if fileName:
            self.graph, self.nodo_lista = self.loadGraphFromCSV(fileName)
            self.plotGraph(self.graph, self.webViewOriginal, 'graph.html')
    
    def loadGraphFromCSV(self, filename):
        nodo_lista = defaultdict(list)
        with open(filename, 'r') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                node = row[0]
                adjacency_list = row[1:] if len(row) > 1 else []
                nodo_lista[node] = adjacency_list
        
        graph = nx.DiGraph(nodo_lista)
        return graph, nodo_lista
        
    def plotGraph(self, graph, web_view, file_name):
    # Se agrega directed=True para hacer el gráfico dirigido
        net = Network(notebook=True, height="750px", width="100%", bgcolor="#222222", font_color="white", directed=True)
        net.from_nx(graph)    

        temp_file = os.path.join(os.getcwd(), file_name)
        net.save_graph(temp_file)
        
        web_view.setUrl(QUrl.fromLocalFile(temp_file))
    
    def findSCCs(self):
        sccs = self.kosaraju(self.nodo_lista)
        self.showSCCs(sccs)
    
    def kosaraju(self, graph):
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
    
    def showSCCs(self, sccs):
        # Crear un grafo solo con los SCCs encontrados
        scc_graph = nx.DiGraph()
        colors = ['#FF5733', '#33FF57', '#5733FF', '#FF33EC', '#33ECFF', '#A633FF', '#FFB933', '#33FFEC']

        # Crear un mapeo de colores para cada nodo en SCCs
        node_color = {}
        color_index = 0

        for scc in sccs:
            current_color = colors[color_index % len(colors)]
            for node in scc:
                node_color[node] = current_color
            color_index += 1

        for scc in sccs:
            if len(scc) > 1:
                for node in scc:
                    for neighbor in self.nodo_lista[node]:
                        if neighbor in scc:
                            scc_graph.add_edge(node, neighbor)

        # Agregar nodos y aristas al grafo con sus colores
        net = Network(notebook=True, height="750px", width="100%", bgcolor="#222222", font_color="white", directed=True)
        for node in scc_graph.nodes():
            net.add_node(node, label=node, color=node_color.get(node, '#FFFFFF'))

        for edge in scc_graph.edges():
            net.add_edge(edge[0], edge[1])

        # Guardar el grafo en un archivo temporal
        temp_file = os.path.join(os.getcwd(), 'scc_graph.html')
        net.save_graph(temp_file)

        # Mostrar el gráfico en el QWebEngineView
        self.webViewSCC.setUrl(QUrl.fromLocalFile(temp_file))

        # Opcional: Guardar SCCs en un archivo CSV
        with open('sccs.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for scc in sccs:
                writer.writerow(scc)
        print("SCCs guardados en sccs.csv")

    def findConnectedComponents(self):
        connected_components = self.unionFind(self.nodo_lista)
        self.showConnectedComponents(connected_components)
    
    def unionFind(self, graph):
        parent = {}
        rank = {}
        followers = {node: len(adj) for node, adj in graph.items()}

        def find(node):
            if parent[node] != node:
                parent[node] = find(parent[node])
            return parent[node]

        def union(node1, node2):
            root1 = find(node1)
            root2 = find(node2)
            if root1 != root2:
                if rank[root1] > rank[root2]:
                    parent[root2] = root1
                elif rank[root1] < rank[root2]:
                    parent[root1] = root2
                else:
                    parent[root2] = root1
                    rank[root1] += 1
        
        for node in graph:
            parent[node] = node
            rank[node] = 0

        for node in graph:
            for neighbor in graph[node]:
                union(node, neighbor)

        components = defaultdict(list)
        for node in graph:
            root = find(node)
            components[root].append(node)
        
        # Reasignar el nodo raíz al nodo con más seguidores dentro del componente
        for root, nodes in components.items():
            max_followers_node = max(nodes, key=lambda node: followers[node])
            new_component = {max_followers_node: nodes}
            components[root] = new_component

        return list(components.values())

    def showConnectedComponents(self, connected_components):
        # Crear un grafo solo con los componentes conectados encontrados
        connected_graph = nx.DiGraph()
        for component in connected_components:
            for root, nodes in component.items():
                for node in nodes:
                    for neighbor in self.nodo_lista[node]:
                        if neighbor in nodes:
                            connected_graph.add_edge(node, neighbor)
        
        # Mostrar el grafo de los componentes conectados en la tercera vista web
        self.plotGraph(connected_graph, self.webViewConnectedComponents, 'connected_graph.html')
        
        # Opcional: Guardar componentes conectados en un archivo CSV
        with open('connected_components.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for component in connected_components:
                for root, nodes in component.items():
                    writer.writerow(nodes)
        print("Componentes conectados guardados en connected_components.csv")
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GraphApp()
    ex.show()
    sys.exit(app.exec_())
