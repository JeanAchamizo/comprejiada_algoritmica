import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
import os
from datasetconfiguration import DatasetConfiguration
from AboutProgram import AboutProgram
from StronglyConnectedComponentsApp import StronglyConnectedComponentsApp  # Importa la nueva clase

class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Know Your Business')
        self.setFixedSize(400, 300)
        self.setStyleSheet('background-color: white;')
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        self.title = QLabel('Know Your Business', self)
        self.title.setStyleSheet('font-size: 24px; font-weight: bold;')
        layout.addWidget(self.title)
        
        self.button1 = QPushButton('Analizar Datos', self)
        self.button1.setStyleSheet('padding: 10px; font-size: 16px;')
        self.button1.clicked.connect(self.showStronglyConnectedComponents)
        layout.addWidget(self.button1)
        
        self.button2 = QPushButton('Seleccionar datos', self)
        self.button2.setStyleSheet('padding: 10px; font-size: 16px;')
        self.button2.clicked.connect(self.selectData)
        layout.addWidget(self.button2)
        
        self.button3 = QPushButton('Acerca del programa', self)
        self.button3.setStyleSheet('padding: 10px; font-size: 16px;')
        self.button3.clicked.connect(self.aboutProgram)
        layout.addWidget(self.button3)
        
        self.button4 = QPushButton('Componentes Fuertemente Conexos', self)  # Nuevo botón
        self.button4.setStyleSheet('padding: 10px; font-size: 16px;')
        self.button4.clicked.connect(self.showSCCApp)
        layout.addWidget(self.button4)
        
        self.setLayout(layout)
    
    def showStronglyConnectedComponents(self):
        # Ejecutar el código para mostrar datos fuertemente conexos
        os.system('python primerapantalla.py')  # Ruta de la pantalla principal
        
    def showSCCApp(self):
        self.sccApp = StronglyConnectedComponentsApp()
        self.sccApp.show()
    
    def selectData(self):
        self.datasetConfig = DatasetConfiguration()
        self.datasetConfig.show()
    
    def aboutProgram(self):
        self.aboutProgram = AboutProgram()
        self.aboutProgram.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainMenu = MainMenu()
    mainMenu.show()
    sys.exit(app.exec_())
