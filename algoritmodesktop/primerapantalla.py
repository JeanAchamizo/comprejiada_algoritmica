import sys
import csv
from collections import defaultdict
import networkx as nx
from pyvis.network import Network
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLabel, QListWidget, QLineEdit
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
        
        mainLayout.addLayout(graphsLayout)

        # Sección para mostrar los padres de cada SCC
        sccParentLayout = QVBoxLayout()
        sccParentLayout.setSpacing(0)
        sccParentLayout.setContentsMargins(0, 0, 0, 0)
        self.sccParentLabel = QLabel('Padres de cada componente fuertemente conexo:')
        self.sccParentLabel.setFixedSize(400, 23)
        sccParentLayout.addWidget(self.sccParentLabel)
        self.sccParentList = QListWidget()
        sccParentLayout.addWidget(self.sccParentList)

        

        mainLayout.addLayout(sccParentLayout)
        
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
        scc_graph = nx.DiGraph()
        colors = ['#FF5733', '#33FF57', '#5733FF', '#FF33EC', '#33ECFF', '#A633FF', '#FFB933', '#33FFEC']
        parent_color = '#FFD700'  # Color dorado para los nodos padre
        
        followers_count = {node: sum([1 for n in self.nodo_lista if node in self.nodo_lista[n]]) for node in self.nodo_lista}
        
        for scc in sccs:
            for node in scc:
                if node not in followers_count:
                    followers_count[node] = 0
        
        node_color = {}
        color_index = 0
        scc_parents = {}
        
        for scc in sccs:
            current_color = colors[color_index % len(colors)]
            max_followers = -1
            parent_node = None
            
            for node in scc:
                node_color[node] = current_color
                if followers_count[node] > max_followers:
                    max_followers = followers_count[node]
                    parent_node = node
            
            scc_parents[parent_node] = scc
            node_color[parent_node] = parent_color
            color_index += 1

        self.sccParentList.clear()
        with open('scc_parents.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for parent in scc_parents:
                self.sccParentList.addItem(f"Padre: {parent}, Seguidores: {followers_count[parent]}")
                writer.writerow([parent, followers_count[parent]])
        
        with open('sccs.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for scc in sccs:
                writer.writerow(scc)
        
        for parent, nodes in scc_parents.items():
            for node in nodes:
                if node != parent:
                    for neighbor in self.nodo_lista[node]:
                        if neighbor in nodes:
                            scc_graph.add_edge(node, neighbor)
        
        net = Network(notebook=True, height="750px", width="100%", bgcolor="#222222", font_color="white", directed=True)
        
        for node in scc_graph.nodes:
            net.add_node(node, color=node_color[node])
        
        for edge in scc_graph.edges:
            net.add_edge(edge[0], edge[1])
        
        temp_file = os.path.join(os.getcwd(), 'scc_graph.html')
        net.save_graph(temp_file)
        
        self.webViewSCC.setUrl(QUrl.fromLocalFile(temp_file))
        
        print("SCCs guardados en sccs.csv")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GraphApp()
    ex.show()
    sys.exit(app.exec_())
