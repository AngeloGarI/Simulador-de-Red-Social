from PyQt6.QtWidgets import *

class Pantalla(QWidget):
    def __init__(self,main):
        super().__init__()
        self.main = main
        layout = QVBoxLayout()
        btn_dark = QPushButton("Modo oscuro")
        btn_dark.clicked.connect(self.dark)
        btn_light = QPushButton("Modo claro")
        btn_light.clicked.connect(self.light)
        layout.addWidget(btn_dark)
        layout.addWidget(btn_light)
        self.setLayout(layout)

    def dark(self):
        self.main.setStyleSheet(
        "background:#18191a;color:white;"
        )

    def light(self):
        self.main.setStyleSheet("")