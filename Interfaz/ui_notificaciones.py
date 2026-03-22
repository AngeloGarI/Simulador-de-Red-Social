from PyQt6.QtWidgets import *
from database import cursor,conn

class Notificaciones(QWidget):


    def __init__(self,usuario):

        super().__init__()

        self.usuario = usuario

        self.setWindowTitle("🔔 Notificaciones")
        self.resize(350,500)

        layout = QVBoxLayout()

        titulo = QLabel("Notificaciones")
        titulo.setStyleSheet("font-size:18px; font-weight:bold;")

        self.lista = QListWidget()

        btn_eliminar = QPushButton("🗑 Eliminar notificación")
        btn_eliminar.clicked.connect(self.eliminar)

        layout.addWidget(titulo)
        layout.addWidget(self.lista)
        layout.addWidget(btn_eliminar)

        self.setLayout(layout)

        self.cargar()

    def cargar(self):

        self.lista.clear()

        try:
            cursor.execute(
            "SELECT id, mensaje FROM notificaciones WHERE usuario=?",
            (self.usuario,)
            )

            datos = cursor.fetchall()

            if not datos:
                self.lista.addItem("No tienes notificaciones")

            for id,mensaje in datos:
                item = QListWidgetItem(mensaje)
                item.setData(1000, id)
                self.lista.addItem(item)

        except Exception as e:
            print("Error cargando notificaciones:", e)

    def eliminar(self):

        item = self.lista.currentItem()

        if item is None:
            return

        id_not = item.data(1000)

        try:
            cursor.execute(
            "DELETE FROM notificaciones WHERE id=?",
            (id_not,)
            )

            conn.commit()

            self.cargar()

        except Exception as e:
            print("Error eliminando:", e)

