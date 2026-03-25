from PyQt6.QtWidgets import *

class Ayuda(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Ayuda y soporte técnico")

        layout = QVBoxLayout()

        texto = QLabel(
        "Para recibir ayuda a soporte técnico contacta a:\n\n"
        "4560-7604\n"
        "4958-0201\n"
        "3067-8267"
        )

        layout.addWidget(texto)

        self.setLayout(layout)
