from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt

class Amigos(QWidget):

    def __init__(self,usuario):

        super().__init__()

        self.usuario = usuario

        self.setWindowTitle("Amigos")
        self.resize(300,400)

        layout = QVBoxLayout()

        self.lista = QListWidget()

        self.lista.addItem("Carlos")
        self.lista.addItem("Ana")
        self.lista.addItem("Luis")

        btn_chat = QPushButton("Abrir chat")
        btn_chat.clicked.connect(self.abrir_chat)

        layout.addWidget(QLabel("Lista de amigos"))
        layout.addWidget(self.lista)
        layout.addWidget(btn_chat)

        self.setLayout(layout)


    def abrir_chat(self):

        item = self.lista.currentItem()

        if item is None:
            QMessageBox.warning(self,"Error","Selecciona un amigo")
            return

        nombre = item.text()

        try:
            from ui_chat import Chat

            self.chat_window = Chat(self.usuario, nombre)
            self.chat_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
            self.chat_window.show()

        except Exception as e:
            print("Error al abrir chat:", e)
            QMessageBox.critical(self,"Error",str(e))



