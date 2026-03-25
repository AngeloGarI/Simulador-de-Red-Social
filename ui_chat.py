import json
import os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt

class Chat(QWidget):
    def __init__(self, usuario, amigo):
        super().__init__()
        self.usuario = usuario
        self.amigo = amigo

        # Clave única para la conversación (orden alfabético)
        self.clave = "_".join(sorted([usuario, amigo]))

        base = os.path.dirname(os.path.abspath(__file__))
        self.archivo = os.path.join(base, "..", "data", "chats.json")

        self.setWindowTitle(f"💬 Chat con {amigo}")
        self.resize(420, 520)

        layout = QVBoxLayout()

        titulo = QLabel(f"💬 {amigo}")
        titulo.setStyleSheet("font-weight:bold; font-size:15px; padding:6px;")
        layout.addWidget(titulo)

        self.lista = QListWidget()
        self.lista.setStyleSheet("border:none;")
        layout.addWidget(self.lista)

        fila = QHBoxLayout()
        self.mensaje = QLineEdit()
        self.mensaje.setPlaceholderText("Escribe un mensaje...")
        self.mensaje.setStyleSheet(
            "border:1px solid #ccc; border-radius:20px; padding:8px 14px;")
        self.mensaje.returnPressed.connect(self.enviar)

        btn = QPushButton("➤")
        btn.setFixedSize(40, 40)
        btn.setStyleSheet("""
            QPushButton { background:#1877f2; color:white;
                border-radius:20px; font-size:16px; }
            QPushButton:hover { background:#166fe5; }
        """)
        btn.clicked.connect(self.enviar)

        fila.addWidget(self.mensaje)
        fila.addWidget(btn)
        layout.addLayout(fila)

        self.setLayout(layout)
        self.cargar()

    def _leer_chats(self):
        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _guardar_chats(self, data):
        os.makedirs(os.path.dirname(self.archivo), exist_ok=True)
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def cargar(self):
        self.lista.clear()
        data = self._leer_chats()
        mensajes = data.get(self.clave, [])
        for msg in mensajes:
            es_mio = msg["de"] == self.usuario
            item = QListWidgetItem(
                f"{'Tú' if es_mio else self.amigo}: {msg['texto']}")
            item.setTextAlignment(
                Qt.AlignmentFlag.AlignRight if es_mio
                else Qt.AlignmentFlag.AlignLeft)
            self.lista.addItem(item)
        self.lista.scrollToBottom()

    def enviar(self):
        texto = self.mensaje.text().strip()
        if not texto:
            return
        data = self._leer_chats()
        if self.clave not in data:
            data[self.clave] = []
        data[self.clave].append({"de": self.usuario, "texto": texto})
        self._guardar_chats(data)
        self.mensaje.clear()
        self.cargar()