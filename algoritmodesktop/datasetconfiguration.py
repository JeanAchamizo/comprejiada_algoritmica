import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox
import pandas as pd
import csv

class DatasetConfiguration(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Configuración del Conjunto de Datos')
        self.resize(400, 200)
        
        mainLayout = QVBoxLayout()
        
        self.fileLabel = QLabel('Archivo de entrada:')
        mainLayout.addWidget(self.fileLabel)
        
        fileLayout = QHBoxLayout()
        self.fileInput = QLineEdit("twitter_combined.txt.gz")
        fileLayout.addWidget(self.fileInput)
        self.browseButton = QPushButton('Examinar')
        self.browseButton.clicked.connect(self.browseFile)
        fileLayout.addWidget(self.browseButton)
        mainLayout.addLayout(fileLayout)
        
        self.rangeLabel = QLabel('Rango de nodos:')
        mainLayout.addWidget(self.rangeLabel)
        
        rangeLayout = QHBoxLayout()
        self.startIndexInput = QLineEdit()
        self.startIndexInput.setPlaceholderText("Inicio")
        rangeLayout.addWidget(self.startIndexInput)
        
        self.endIndexInput = QLineEdit()
        self.endIndexInput.setPlaceholderText("Final")
        rangeLayout.addWidget(self.endIndexInput)
        
        mainLayout.addLayout(rangeLayout)
        
        self.outputLabel = QLabel('Nombre del archivo de salida:')
        mainLayout.addWidget(self.outputLabel)
        
        self.outputInput = QLineEdit()
        mainLayout.addWidget(self.outputInput)
        
        self.runButton = QPushButton('Ejecutar')
        self.runButton.clicked.connect(self.runProcess)
        mainLayout.addWidget(self.runButton)
        
        self.setLayout(mainLayout)
    
    def browseFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Seleccionar Archivo", "", "Archivos GZIP (*.gz);;Todos los archivos (*)", options=options)
        if fileName:
            self.fileInput.setText(fileName)
    
    def runProcess(self):
        input_file = self.fileInput.text()
        try:
            start_index = int(self.startIndexInput.text())
            end_index = int(self.endIndexInput.text())
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Los índices de rango deben ser enteros')
            return
        
        output_file = self.outputInput.text()
        
        if not input_file or not output_file or start_index < 0 or end_index <= start_index:
            QMessageBox.warning(self, 'Error', 'Todos los campos son obligatorios y los índices deben ser válidos')
            return
        
        self.processData(input_file, output_file, start_index, end_index)
    
    def processData(self, input_file, output_file, start_index, end_index):
        twitter = pd.read_csv(input_file, compression="gzip", sep=" ", names=["start_node", "end_node"])
        
        twitter_adj_list = self.dataframe_to_adjacency_list(twitter, "start_node", "end_node")
        
        ranged_nodes_adj_list = self.reduce_to_range_nodes(twitter_adj_list, start_index, end_index)
        
        cleaned_adj_list = self.clean_adjacency_list(ranged_nodes_adj_list)
        
        self.save_adjacency_list_to_csv(cleaned_adj_list, output_file)
        
        QMessageBox.information(self, 'Éxito', f'Archivo guardado como {output_file}')
    
    def dataframe_to_adjacency_list(self, dataframe, start_col, end_col):
        adjacency_list = {}
        for index, row in dataframe.iterrows():
            start_node = row[start_col]
            end_node = row[end_col]
            
            if start_node not in adjacency_list:
                adjacency_list[start_node] = []
            adjacency_list[start_node].append(end_node)
        return adjacency_list
    
    def reduce_to_range_nodes(self, adjacency_list, start_index, end_index):
        # Convertir los items del diccionario a una lista para poder indexar
        items_list = list(adjacency_list.items())
        # Seleccionar el rango de nodos directamente sin ordenar
        range_nodes = items_list[start_index:end_index]
        # Convertir la lista de nodos seleccionados de vuelta a un diccionario
        reduced_adj_list = dict(range_nodes)
        return reduced_adj_list
    
    def clean_adjacency_list(self, adjacency_list):
        keys = set(adjacency_list.keys())
        cleaned_list = {}
        for node, neighbors in adjacency_list.items():
            filtered_neighbors = [neighbor for neighbor in neighbors if neighbor in keys and neighbor != node]
            if filtered_neighbors:
                cleaned_list[node] = filtered_neighbors
        
        # Segundo filtrado para eliminar nodos no conectados
        final_list = {node: neighbors for node, neighbors in cleaned_list.items() if any(node in nlist for nlist in cleaned_list.values())}
        
        return final_list
    
    def save_adjacency_list_to_csv(self, adjacency_list, filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for node, neighbors in adjacency_list.items():
                writer.writerow([node] + neighbors)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    datasetConfig = DatasetConfiguration()
    datasetConfig.show()
    sys.exit(app.exec_())
