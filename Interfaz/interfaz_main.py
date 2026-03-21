import sys
from PyQt6.QtWidgets import QApplication
from database import inicializar
from ui_login import Login

print("Fakebook inicializado.")

inicializar()

app = QApplication(sys.argv)

login = Login()
login.show()

sys.exit(app.exec())