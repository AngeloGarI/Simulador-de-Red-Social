from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from database import cursor,conn
from ui_feed import Feed

class Login(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Fakebook")
        self.resize(400,420)

        self.setStyleSheet("background:#1877f2")

        layout = QVBoxLayout()

        titulo = QLabel("Fakebook")
        titulo.setFont(QFont("Arial",34,QFont.Weight.Bold))
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
        btn_crear = QPushButton("Crear cuenta")

        btn_login.clicked.connect(self.login)
        btn_crear.clicked.connect(self.crear)

        layout.addWidget(titulo)
        layout.addWidget(subtitulo)
        layout.addSpacing(30)
        layout.addWidget(self.user)
        layout.addWidget(self.password)
        layout.addWidget(btn_login)
        layout.addWidget(btn_crear)

        self.setLayout(layout)

    def login(self):

        u = self.user.text()
        p = self.password.text()

        cursor.execute(
        "SELECT * FROM usuarios WHERE usuario=? AND password=?",
        (u,p)
        )

        if cursor.fetchone():

            print("Sesión iniciada")

            self.feed = Feed(u)
            self.feed.show()

            self.close()

        else:

            QMessageBox.warning(self,"Error","Credenciales incorrectas")

    def crear(self):

        u = self.user.text()
        p = self.password.text()

        try:

            cursor.execute(
            "INSERT INTO usuarios(usuario,password) VALUES (?,?)",
            (u,p)
            )

            conn.commit()

            QMessageBox.information(self,"Éxito","Cuenta creada")

        except:

            QMessageBox.warning(self,"Error","Usuario ya existe")