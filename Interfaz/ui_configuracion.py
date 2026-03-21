from PyQt6.QtWidgets import *

class Configuracion(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Configuración y privacidad")

        layout = QVBoxLayout()

        layout.addWidget(QCheckBox("Mostrar estado en línea"))
        layout.addWidget(QCheckBox("Permitir mensajes de desconocidos"))

        layout.addWidget(QPushButton("Guardar"))

        self.setLayout(layout)

