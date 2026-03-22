from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt

class Amigos(QWidget):
    def __init__(self, usuario, um):
        super().__init__()
        self.usuario = usuario
        self.um = um
        self.setWindowTitle("👥 Amigos")
        self.resize(400, 550)

        layout = QVBoxLayout()

        # ── Solicitudes recibidas ──────────────────────────────
        lbl_sol = QLabel("📩 Solicitudes de amistad")
        lbl_sol.setStyleSheet("font-weight:bold; font-size:14px;")
        layout.addWidget(lbl_sol)

        self.lista_solicitudes = QListWidget()
        self.lista_solicitudes.setMaximumHeight(140)
        layout.addWidget(self.lista_solicitudes)

        btn_aceptar  = QPushButton("✅ Aceptar")
        btn_rechazar = QPushButton("❌ Rechazar")
        btn_aceptar.clicked.connect(self.aceptar)
        btn_rechazar.clicked.connect(self.rechazar)

        row_sol = QHBoxLayout()
        row_sol.addWidget(btn_aceptar)
        row_sol.addWidget(btn_rechazar)
        layout.addLayout(row_sol)

        # ── Lista de amigos ────────────────────────────────────
        lbl_amigos = QLabel("👥 Mis amigos")
        lbl_amigos.setStyleSheet("font-weight:bold; font-size:14px; margin-top:10px;")
        layout.addWidget(lbl_amigos)

        self.lista_amigos = QListWidget()
        layout.addWidget(self.lista_amigos)

        btn_chat = QPushButton("💬 Abrir chat")
        btn_chat.clicked.connect(self.abrir_chat)
        layout.addWidget(btn_chat)

        self.setLayout(layout)
        self.cargar()

    def cargar(self):
        # Solicitudes
        self.lista_solicitudes.clear()
        for s in self.um.get_solicitudes_recibidas(self.usuario):
            self.lista_solicitudes.addItem(s)
        if self.lista_solicitudes.count() == 0:
            self.lista_solicitudes.addItem("Sin solicitudes pendientes")

        # Amigos
        self.lista_amigos.clear()
        for a in self.um.get_amigos(self.usuario):
            self.lista_amigos.addItem(f"🟢 {a}")
        if self.lista_amigos.count() == 0:
            self.lista_amigos.addItem("Aún no tienes amigos")

    def aceptar(self):
        item = self.lista_solicitudes.currentItem()
        if not item or item.text() == "Sin solicitudes pendientes":
            QMessageBox.warning(self, "Error", "Selecciona una solicitud")
            return
        de = item.text()
        if self.um.aceptar_solicitud(self.usuario, de):
            QMessageBox.information(self, "✅", f"Ahora eres amigo de {de}")
            self.cargar()
        else:
            QMessageBox.warning(self, "Error", "No se pudo aceptar")

    def rechazar(self):
        item = self.lista_solicitudes.currentItem()
        if not item or item.text() == "Sin solicitudes pendientes":
            QMessageBox.warning(self, "Error", "Selecciona una solicitud")
            return
        de = item.text()
        self.um.rechazar_solicitud(self.usuario, de)
        QMessageBox.information(self, "✅", f"Solicitud de {de} rechazada")
        self.cargar()

    def abrir_chat(self):
        item = self.lista_amigos.currentItem()
        if not item or item.text() == "Aún no tienes amigos":
            QMessageBox.warning(self, "Error", "Selecciona un amigo")
            return
        nombre = item.text().replace("🟢 ", "").strip()
        from ui_chat import Chat
        self.chat_window = Chat(self.usuario, nombre)
        self.chat_window.show()