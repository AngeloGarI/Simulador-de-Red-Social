from PyQt6.QtWidgets import *

class Notificaciones(QWidget):
    def __init__(self, usuario, um):
        super().__init__()
        self.usuario = usuario
        self.um = um
        self.setWindowTitle("🔔 Notificaciones")
        self.resize(380, 450)

        layout = QVBoxLayout()

        titulo = QLabel("🔔 Notificaciones")
        titulo.setStyleSheet("font-size:18px; font-weight:bold;")
        layout.addWidget(titulo)

        self.lista = QListWidget()
        layout.addWidget(self.lista)

        btn_limpiar = QPushButton("🗑 Limpiar todas")
        btn_limpiar.clicked.connect(self.limpiar)
        layout.addWidget(btn_limpiar)

        self.setLayout(layout)
        self.cargar()

    def cargar(self):
        self.lista.clear()
        notifs = []

        # Solicitudes recibidas → notificación real
        for s in self.um.get_solicitudes_recibidas(self.usuario):
            notifs.append(f"👥 {s} te envió solicitud de amistad")

        # Amigos nuevos (los que están en amigos)
        for a in self.um.get_amigos(self.usuario):
            notifs.append(f"✅ {a} es tu amigo")

        if notifs:
            for n in notifs:
                self.lista.addItem(n)
        else:
            self.lista.addItem("Sin notificaciones")

    def limpiar(self):
        self.lista.clear()
        self.lista.addItem("Sin notificaciones")