import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

# Obtener la ruta absoluta del directorio actual
current_directory = os.path.dirname(os.path.abspath(__file__))

# Construir la ruta completa al archivo HTML
html_file_path = os.path.join(current_directory, "graph.html")
print(html_file_path)
app = QApplication([])
webView = QWebEngineView()

# Usar QUrl.fromLocalFile para convertir la ruta a una URL
webView.setUrl(QUrl.fromLocalFile(html_file_path))

webView.show()
app.exec_()