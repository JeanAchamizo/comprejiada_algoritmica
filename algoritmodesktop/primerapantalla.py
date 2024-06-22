import sys
import csv
from collections import defaultdict
import networkx as nx
from pyvis.network import Network
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLabel, QTableWidget, QTableWidgetItem,QSizePolicy
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
        # Layout principal vertical
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(10, 10, 10, 10)  # Eliminar márgenes
        mainLayout.setSpacing(0)  # Eliminar espacio entre widgets
        

        # Cambiar el layout de los botones a QHBoxLayout para que estén lado a lado
        buttonsLayout = QHBoxLayout()
        buttonsLayout.setSpacing(0)  # Eliminar espacio entre widgets
        self.label = QLabel('Sube tu archivo:')        
        buttonsLayout.addWidget(self.label)
        self.uploadButton = QPushButton('Enviar archivo')
        self.uploadButton.clicked.connect(self.loadCSV)
        buttonsLayout.addWidget(self.uploadButton)
        self.sccButton = QPushButton('Encontrar componentes fuertemente conexos')
        self.sccButton.clicked.connect(self.findSCCs)
        buttonsLayout.addWidget(self.sccButton)
        # Agregar el layout de botones al layout principal
        mainLayout.addLayout(buttonsLayout)

        # Layout horizontal para las gráficas
        graphsLayout = QHBoxLayout()
        graphsLayout.setSpacing(0)  # Eliminar espacio entre layouts
        graphsLayout.setContentsMargins(0, 0, 0, 0)  # Eliminar márgenes
        
        # Layout para la gráfica original
        originalGraphLayout = QVBoxLayout()
        originalGraphLayout.setSpacing(0)  # Eliminar espacio entre widgets
        originalGraphLayout.setContentsMargins(0, 0, 5, 0)  # Eliminar márgenes
        self.graphLabel = QLabel('Grafo de los datos del archivo:')
        self.graphLabel.setFixedSize(600, 23) # Establecer tamaño fijo para el label
        originalGraphLayout.addWidget(self.graphLabel)
        self.webViewOriginal = QWebEngineView()
        originalGraphLayout.addWidget(self.webViewOriginal)
        graphsLayout.addLayout(originalGraphLayout)
        
        # Layout para la gráfica de los SCCs
        sccGraphLayout = QVBoxLayout()
        sccGraphLayout.setSpacing(0)  # Eliminar espacio entre widgets
        sccGraphLayout.setContentsMargins(0, 0, 0, 0)  # Eliminar márgenes
        self.sccGraphLabel = QLabel('Grafo de los componentes fuertemente conexos:')
        self.sccGraphLabel.setFixedSize(600, 23)  # Establecer tamaño fijo para el label
        sccGraphLayout.addWidget(self.sccGraphLabel)
        self.webViewSCC = QWebEngineView()
        sccGraphLayout.addWidget(self.webViewSCC)
        graphsLayout.addLayout(sccGraphLayout)
        
        # Agregar el layout de las gráficas al layout principal
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
        print("SCCs guardados en sccs.csv")
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GraphApp()
    ex.show()
    sys.exit(app.exec_())
