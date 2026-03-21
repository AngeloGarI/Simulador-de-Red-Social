from PyQt6.QtWidgets import *
from database import cursor,conn
from datetime import datetime

class Chat(QWidget):

    def __init__(self,usuario,amigo):

        super().__init__()

        self.usuario = usuario
        self.amigo = amigo

        self.setWindowTitle(f"Chat con {amigo}")
        self.resize(400,500)

        layout = QVBoxLayout()

        self.lista = QListWidget()

        self.mensaje = QLineEdit()

        btn = QPushButton("Enviar")
        btn.clicked.connect(self.enviar)

        layout.addWidget(self.lista)
        layout.addWidget(self.mensaje)
        layout.addWidget(btn)

        self.setLayout(layout)

        self.cargar()

    def cargar(self):

        self.lista.clear()

        try:
            cursor.execute("""
            SELECT emisor,mensaje FROM mensajes
            WHERE (emisor=? AND receptor=?)
            OR (emisor=? AND receptor=?)
            """,(self.usuario,self.amigo,self.amigo,self.usuario))

            for u,m in cursor.fetchall():
                self.lista.addItem(f"{u}: {m}")

        except Exception as e:
            print("Error cargando chat:", e)

    def enviar(self):

        texto = self.mensaje.text()

        if texto == "":
            return

        try:
            fecha = datetime.now().strftime("%H:%M")

            cursor.execute(
            "INSERT INTO mensajes(emisor,receptor,mensaje,fecha) VALUES (?,?,?,?)",
            (self.usuario,self.amigo,texto,fecha)
            )

            conn.commit()

            self.mensaje.clear()
            self.cargar()

        except Exception as e:
            print("Error enviando mensaje:", e)

