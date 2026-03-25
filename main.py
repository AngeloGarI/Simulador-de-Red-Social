import sys
from PyQt6.QtWidgets import QApplication
from Logica.user_manager import UserManager

if __name__ == "__main__":
    app = QApplication(sys.argv)

    um = UserManager()
    usuario = um.cargar_sesion()

    if usuario:
        from Interfaz.ui_feed import Feed
        ventana = Feed(usuario)
    else:
        from Interfaz.ui_login import Login
        ventana = Login()

    ventana.show()
    sys.exit(app.exec())