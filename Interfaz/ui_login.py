from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt
from Logica.user_manager import UserManager

class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.um = UserManager()
        self.setWindowTitle("Fakebook")
        self.resize(400, 420)
        self.setStyleSheet("background:#1877f2")

        layout = QVBoxLayout()
        titulo = QLabel("Fakebook")
        titulo.setFont(QFont("Arial", 34, QFont.Weight.Bold))
        titulo.setStyleSheet("color:white")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitulo = QLabel("Inicia sesión para continuar")
        subtitulo.setStyleSheet("color:white")
        subtitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.user = QLineEdit()
        self.user.setPlaceholderText("Usuario")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Contraseña")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        btn_login = QPushButton("Iniciar sesión")
        btn_crear = QPushButton("Crear cuenta nueva")
        btn_login.clicked.connect(self.login)
        btn_crear.clicked.connect(self.crear)

        for w in [self.user, self.password]:
            w.setStyleSheet("""
                background:white;
                color:black;
                border-radius:5px;
                padding:8px;
            """)

        for b in [btn_login, btn_crear]:
            b.setStyleSheet("""
                QPushButton { background:white; color:#1877f2;
                    font-weight:bold; border-radius:5px; padding:10px; }
                QPushButton:hover { background:#e7f3ff; }
            """)

        layout.addWidget(titulo)
        layout.addWidget(subtitulo)
        layout.addSpacing(30)
        layout.addWidget(self.user)
        layout.addWidget(self.password)
        layout.addSpacing(10)
        layout.addWidget(btn_login)
        layout.addWidget(btn_crear)
        self.setLayout(layout)

    def login(self):
        u = self.user.text().strip()
        p = self.password.text()
        if not u or not p:
            QMessageBox.warning(self, "Error", "Completa todos los campos")
            return
        usuario = self.um.login(u, p)
        if usuario:
            self.um.guardar_sesion(u)  # ← agregar esta línea
            from Interfaz.ui_feed import Feed
            self.feed = Feed(u)
            self.feed.show()
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos")

    def crear(self):
        u = self.user.text().strip()
        p = self.password.text()
        if not u or not p:
            QMessageBox.warning(self, "Error", "Completa los campos")
            return
        if self.um.registrar(u, p):
            QMessageBox.information(self, "✅ Cuenta creada",
                f"Bienvenido, {u}. Ya puedes iniciar sesión.")
        else:
            QMessageBox.warning(self, "Error", "Ese nombre de usuario ya existe")