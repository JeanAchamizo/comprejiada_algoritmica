import sys
import csv
from collections import defaultdict
import networkx as nx
from pyvis.network import Network
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QListWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt
import os

class StronglyConnectedComponentsApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Componentes Fuertemente Conexos')
        self.resize(1200, 600)
        self.setStyleSheet('background-color: #333; color: white;')
        
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(10, 10, 10, 10)
        mainLayout.setSpacing(10)
        
        buttonsLayout = QHBoxLayout()
        buttonsLayout.setSpacing(10)
        
        self.loadSCCButton = QPushButton('Cargar Grafo Fuertemente Conexo')
        self.loadSCCButton.clicked.connect(self.loadSCCGraph)
        buttonsLayout.addWidget(self.loadSCCButton)
        
        self.unionButton = QPushButton('Unir Componentes')
        self.unionButton.clicked.connect(self.unionFind)
        buttonsLayout.addWidget(self.unionButton)
        
        self.node1Input = QLineEdit(self)
        self.node1Input.setPlaceholderText('Nodo 1')
        buttonsLayout.addWidget(self.node1Input)
        
        self.node2Input = QLineEdit(self)
        self.node2Input.setPlaceholderText('Nodo 2')
        buttonsLayout.addWidget(self.node2Input)
        
        mainLayout.addLayout(buttonsLayout)
        
        graphsLayout = QHBoxLayout()
        graphsLayout.setSpacing(10)
        
        sccGraphLayout = QVBoxLayout()
        sccGraphLayout.setSpacing(10)
        
        self.sccGraphLabel = QLabel('Grafo de los Componentes Fuertemente Conexos:')
        self.sccGraphLabel.setFixedHeight(23)
        sccGraphLayout.addWidget(self.sccGraphLabel)
        
        self.webViewSCC = QWebEngineView()
        sccGraphLayout.addWidget(self.webViewSCC)
        
        graphsLayout.addLayout(sccGraphLayout)
        
        unionGraphLayout = QVBoxLayout()
        unionGraphLayout.setSpacing(10)
        
        self.unionGraphLabel = QLabel('Grafo con Uniones:')
        self.unionGraphLabel.setFixedHeight(23)
        unionGraphLayout.addWidget(self.unionGraphLabel)
        
        self.webViewUnion = QWebEngineView()
        unionGraphLayout.addWidget(self.webViewUnion)
        
        graphsLayout.addLayout(unionGraphLayout)
        
        mainLayout.addLayout(graphsLayout)
        
        self.setLayout(mainLayout)
        
        self.graph = None
        self.nodo_lista = defaultdict(list)
        self.parent = {}
        self.size = {}
        self.unions = []
    
    def loadSCCGraph(self):
        filename = 'sccs.csv'
        self.graph, self.nodo_lista = self.loadGraphFromCSV(filename)
        self.initializeUnionFind()
        self.plotGraph(self.graph, self.webViewSCC, 'scc_graph.html')
    
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
        
    def initializeUnionFind(self):
        for node in self.graph.nodes():
            self.parent[node] = node
            self.size[node] = 1
    
    def plotGraph(self, graph, web_view, file_name):
        net = Network(notebook=True, height="750px", width="100%", bgcolor="#222222", font_color="white", directed=True)
        net.from_nx(graph)    

        temp_file = os.path.join(os.getcwd(), file_name)
        net.save_graph(temp_file)
        
        web_view.setUrl(QUrl.fromLocalFile(temp_file))
    
    def unionFind(self):
        node1 = self.node1Input.text()
        node2 = self.node2Input.text()
        if node1 and node2:
            self.union(node1, node2)
            self.updateUnionGraph()
    
    def find(self, node):
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

    def union(self, node1, node2):
        root1 = self.find(node1)
        root2 = self.find(node2)
        if root1 != root2:
            if self.size[root1] < self.size[root2]:
                self.parent[root1] = root2
                self.size[root2] += self.size[root1]
            else:
                self.parent[root2] = root1
                self.size[root1] += self.size[root2]
            self.unions.append((node1, node2))  # Guardar la unión
    
    def updateUnionGraph(self):
        union_graph = self.graph.copy()
        
        for node1, node2 in self.unions:
            union_graph.add_edge(node1, node2)
        
        self.plotGraph(union_graph, self.webViewUnion, 'union_graph.html')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StronglyConnectedComponentsApp()
    ex.show()
    sys.exit(app.exec_())
