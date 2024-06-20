import sys
import csv
from collections import defaultdict
import networkx as nx
from pyvis.network import Network
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLabel, QTableWidget, QTableWidgetItem
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import os

class GraphApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Grafo de los datos del archivo')
        self.resize(1200, 800)
        
        # Layout principal horizontal
        mainLayout = QHBoxLayout()
        
        # Layout para el lado izquierdo (subir archivo y botones)
        leftLayout = QVBoxLayout()
        
        self.label = QLabel('Sube tu archivo:')
        leftLayout.addWidget(self.label)
        
        self.uploadButton = QPushButton('Enviar archivo')
        self.uploadButton.clicked.connect(self.loadCSV)
        leftLayout.addWidget(self.uploadButton)
        
        self.sccButton = QPushButton('Encontrar componentes fuertemente conexos')
        self.sccButton.clicked.connect(self.findSCCs)
        leftLayout.addWidget(self.sccButton)
        
        # Layout para el lado derecho (visualización de los grafos)
        rightLayout = QVBoxLayout()
        
        self.graphLabel = QLabel('Grafo de los datos del archivo:')
        rightLayout.addWidget(self.graphLabel)
        
        self.webViewOriginal = QWebEngineView()
        rightLayout.addWidget(self.webViewOriginal)
        
        self.sccGraphLabel = QLabel('Grafo de los componentes fuertemente conexos:')
        rightLayout.addWidget(self.sccGraphLabel)
        
        self.webViewSCC = QWebEngineView()
        rightLayout.addWidget(self.webViewSCC)
        
        # Agregar layouts izquierdo y derecho al layout principal
        mainLayout.addLayout(leftLayout)
        mainLayout.addLayout(rightLayout)
        
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
        net = Network(notebook=True, height="750px", width="100%", bgcolor="#222222", font_color="white")
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
        for scc in sccs:
            if len(scc) > 1:
                for node in scc:
                    for neighbor in self.nodo_lista[node]:
                        if neighbor in scc:
                            scc_graph.add_edge(node, neighbor)
        
        # Mostrar el grafo de los SCCs en la segunda vista web
        self.plotGraph(scc_graph, self.webViewSCC, 'scc_graph.html')
        
        # Opcional: Guardar SCCs en un archivo CSV
        with open('sccs.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for scc in sccs:
                writer.writerow(scc)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GraphApp()
    ex.show()
    sys.exit(app.exec_())
