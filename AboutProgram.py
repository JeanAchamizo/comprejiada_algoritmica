import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QTextEdit

class AboutProgram(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Acerca del programa')
        self.resize(400, 300)
        
        mainLayout = QVBoxLayout()
        
        aboutText = QTextEdit()
        aboutText.setReadOnly(True)
        aboutText.setPlainText("""
        Know Your Business - Análisis de Redes Sociales

        Este programa permite analizar redes sociales mediante la reducción de grandes conjuntos de datos a subgrafos más manejables, y la limpieza de las relaciones de estos subgrafos.

        Funcionalidades principales:
        1. Cargar datos: Permite seleccionar y cargar un archivo de datos comprimido (.gz) con información sobre nodos y relaciones.
        2. Seleccionar rango de nodos: Reduce el conjunto de datos original a un subgrafo, seleccionando un rango específico de nodos basándose en el tamaño de sus listas de adyacencia.
        3. Limpiar relaciones: Elimina nodos y relaciones no válidas, asegurando que solo se conserven las relaciones relevantes y conectadas.

        Algoritmo y funciones:

        1. dataframe_to_adjacency_list(dataframe, start_col, end_col):
           Convierte un DataFrame de pandas en una lista de adyacencia, donde cada nodo tiene una lista de nodos conectados.

        2. reduce_to_range_nodes(adjacency_list, start_index, end_index):
           Reduce la lista de adyacencia original a un subgrafo, seleccionando nodos dentro del rango especificado por el usuario.

        3. clean_adjacency_list(adjacency_list):
           Limpia la lista de adyacencia, eliminando nodos sin relaciones válidas y nodos que no están conectados a otros nodos en el subgrafo.

        4. save_adjacency_list_to_csv(adjacency_list, filename):
           Guarda la lista de adyacencia en un archivo CSV, con cada fila representando un nodo y sus nodos conectados.

        Este proceso permite analizar y visualizar subgrafos de grandes redes sociales, facilitando el análisis y la toma de decisiones.
        """)
        
        mainLayout.addWidget(aboutText)
        
        self.setLayout(mainLayout)

if __name__ == '__main__':
      app = QApplication(sys.argv)
      about = AboutProgram()
      about.show()
      sys.exit(app.exec_())