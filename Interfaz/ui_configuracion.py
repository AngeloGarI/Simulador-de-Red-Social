from PyQt6.QtWidgets import *

class Configuracion(QWidget):
    def __init__(self, usuario, um):
        super().__init__()
        self.usuario = usuario
        self.um = um
        self.setWindowTitle("⚙️ Configuración")
        self.resize(380, 400)

        layout = QVBoxLayout()

        titulo = QLabel("⚙️ Configuración y privacidad")
        titulo.setStyleSheet("font-size:16px; font-weight:bold;")
        layout.addWidget(titulo)

        # Cargar config actual
        config = self.um.get_config(usuario)

        self.chk_online = QCheckBox("Mostrar estado en línea")
        self.chk_online.setChecked(config.get("mostrar_en_linea", True))

        self.chk_mensajes = QCheckBox("Permitir mensajes de desconocidos")
        self.chk_mensajes.setChecked(config.get("mensajes_desconocidos", True))

        layout.addSpacing(10)
        layout.addWidget(self.chk_online)
        layout.addWidget(self.chk_mensajes)

        # Cambiar contraseña
        layout.addSpacing(16)
        lbl_pw = QLabel("🔒 Cambiar contraseña")
        lbl_pw.setStyleSheet("font-weight:bold;")
        layout.addWidget(lbl_pw)

        self.pw_actual = QLineEdit()
        self.pw_actual.setPlaceholderText("Contraseña actual")
        self.pw_actual.setEchoMode(QLineEdit.EchoMode.Password)

        self.pw_nueva = QLineEdit()
        self.pw_nueva.setPlaceholderText("Nueva contraseña")
        self.pw_nueva.setEchoMode(QLineEdit.EchoMode.Password)

        btn_pw = QPushButton("Cambiar contraseña")
        btn_pw.clicked.connect(self.cambiar_password)

        layout.addWidget(self.pw_actual)
        layout.addWidget(self.pw_nueva)
        layout.addWidget(btn_pw)

        layout.addStretch()

        btn_guardar = QPushButton("💾 Guardar configuración")
        btn_guardar.setStyleSheet("""
            QPushButton { background:#1877f2; color:white;
                border-radius:8px; padding:10px; font-weight:bold; }
            QPushButton:hover { background:#166fe5; }
        """)
        btn_guardar.clicked.connect(self.guardar)
        layout.addWidget(btn_guardar)

        self.setLayout(layout)

    def guardar(self):
        self.um.guardar_config(self.usuario, {
            "mostrar_en_linea":      self.chk_online.isChecked(),
            "mensajes_desconocidos": self.chk_mensajes.isChecked()
        })
        QMessageBox.information(self, "✅", "Configuración guardada")

    def cambiar_password(self):
        actual = self.pw_actual.text()
        nueva  = self.pw_nueva.text()
        if not actual or not nueva:
            QMessageBox.warning(self, "Error", "Completa ambos campos")
            return
        if self.um.cambiar_password(self.usuario, actual, nueva):
            QMessageBox.information(self, "✅", "Contraseña actualizada")
            self.pw_actual.clear()
            self.pw_nueva.clear()
        else:
            QMessageBox.warning(self, "Error", "Contraseña actual incorrecta")