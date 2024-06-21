import sys
import csv
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

class GraphApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Grafo')
        
        layout = QVBoxLayout()
        
        self.label = QLabel('Sube tu archivo:')
        layout.addWidget(self.label)
        
        self.uploadButton = QPushButton('Enviar archivo')
        self.uploadButton.clicked.connect(self.loadCSV)
        layout.addWidget(self.uploadButton)
        
        self.sccButton = QPushButton('Encontrar componentes fuertemente conexos')
        self.sccButton.clicked.connect(self.findSCCs)
        layout.addWidget(self.sccButton)
        
        self.setLayout(layout)
    
    def loadCSV(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if fileName:
            self.graph, self.nodo_lista = self.loadGraphFromCSV(fileName)
            self.plotGraph(self.graph)
    
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
    
    def plotGraph(self, graph):
        plt.figure(figsize=(8, 6))
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=15, font_weight='bold')
        plt.show()
    
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
        self.sccWindow = QWidget()
        self.sccWindow.setWindowTitle('Componentes Fuertemente Conexos')
        
        layout = QVBoxLayout()
        
        table = QTableWidget()
        table.setRowCount(len(sccs))
        table.setColumnCount(1)
        table.setHorizontalHeaderLabels(['SCCs'])
        
        for i, scc in enumerate(sccs):
            item = QTableWidgetItem(', '.join(scc))
            table.setItem(i, 0, item)
        
        layout.addWidget(table)
        self.sccWindow.setLayout(layout)
        self.sccWindow.show()
        
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
