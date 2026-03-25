import os
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class Perfil(QWidget):
    def __init__(self, usuario, um, solo_lectura=False):
        super().__init__()
        self.usuario     = usuario
        self.um          = um
        self.solo_lectura = solo_lectura
        self.setWindowTitle("👤 Perfil")
        self.resize(420, 520)

        layout = QVBoxLayout()
        layout.setSpacing(12)

        u = self.um.buscar(usuario)

        # ── Avatar grande ──────────────────────────────────────
        self.lbl_foto = QLabel()
        self.lbl_foto.setFixedSize(90, 90)
        self.lbl_foto.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._actualizar_avatar(u)

        avatar_row = QHBoxLayout()
        avatar_row.addStretch()
        avatar_row.addWidget(self.lbl_foto)
        avatar_row.addStretch()
        layout.addLayout(avatar_row)

        if not solo_lectura:
            btn_foto = QPushButton("📷 Cambiar foto")
            btn_foto.setStyleSheet("""
                QPushButton { background:transparent; color:#1877f2;
                    border:none; font-size:13px; }
                QPushButton:hover { text-decoration:underline; }
            """)
            btn_foto.clicked.connect(self.cambiar_foto)
            foto_row = QHBoxLayout()
            foto_row.addStretch()
            foto_row.addWidget(btn_foto)
            foto_row.addStretch()
            layout.addLayout(foto_row)

        # ── Info ───────────────────────────────────────────────
        lbl_username = QLabel(f"@{usuario}")
        lbl_username.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_username.setStyleSheet("color:gray; font-size:13px;")
        layout.addWidget(lbl_username)

        # Estadísticas
        amigos    = self.um.get_amigos(usuario)
        guardados = self.um.get_guardados(usuario)
        stats_row = QHBoxLayout()
        for valor, etiqueta in [(len(amigos), "Amigos"), (len(guardados), "Guardados")]:
            col = QVBoxLayout()
            lv = QLabel(str(valor))
            lv.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lv.setStyleSheet("font-size:20px; font-weight:bold;")
            le = QLabel(etiqueta)
            le.setAlignment(Qt.AlignmentFlag.AlignCenter)
            le.setStyleSheet("color:gray; font-size:12px;")
            col.addWidget(lv)
            col.addWidget(le)
            stats_row.addLayout(col)
        layout.addLayout(stats_row)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color:#e4e6eb;")
        layout.addWidget(sep)

        if not solo_lectura:
            # Campos editables
            lbl_n = QLabel("Nombre:")
            self.inp_nombre = QLineEdit(u["nombre"] if u else "")
            lbl_b = QLabel("Bio:")
            self.inp_bio = QTextEdit()
            self.inp_bio.setFixedHeight(70)
            self.inp_bio.setPlaceholderText("Cuéntanos algo sobre ti...")
            if u:
                self.inp_bio.setPlainText(u.get("bio", ""))
            layout.addWidget(lbl_n)
            layout.addWidget(self.inp_nombre)
            layout.addWidget(lbl_b)
            layout.addWidget(self.inp_bio)
            layout.addStretch()

            btn_guardar = QPushButton("💾 Guardar perfil")
            btn_guardar.setStyleSheet("""
                QPushButton { background:#1877f2; color:white;
                    border-radius:8px; padding:10px; font-weight:bold; }
                QPushButton:hover { background:#166fe5; }
            """)
            btn_guardar.clicked.connect(self.guardar)
            layout.addWidget(btn_guardar)
        else:
            # Solo lectura: mostrar bio y botón agregar amigo
            bio = u.get("bio", "") if u else ""
            lbl_bio = QLabel(bio or "Sin bio")
            lbl_bio.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_bio.setWordWrap(True)
            lbl_bio.setStyleSheet("color:gray; font-size:13px;")
            layout.addWidget(lbl_bio)
            layout.addStretch()

        self.setLayout(layout)

    def _actualizar_avatar(self, u):
        foto = u.get("foto", "") if u else ""
        if foto and os.path.exists(foto):
            from PyQt6.QtGui import QPainter, QBrush, QColor, QPixmap, QPainterPath
            # Crear canvas transparente de 90x90
            resultado = QPixmap(90, 90)
            resultado.fill(QColor(0, 0, 0, 0))  # totalmente transparente

            # Cargar y escalar la foto
            original = QPixmap(foto).scaled(
                90, 90,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation)

            # Centrar si es más grande
            x = (original.width() - 90) // 2
            y = (original.height() - 90) // 2
            original = original.copy(x, y, 90, 90)

            # Dibujar con clip circular
            painter = QPainter(resultado)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            path = QPainterPath()
            path.addEllipse(0, 0, 90, 90)
            painter.setClipPath(path)
            painter.drawPixmap(0, 0, original)
            painter.end()

            self.lbl_foto.setPixmap(resultado)
            self.lbl_foto.setStyleSheet("background:transparent; border-radius:45px;")
        else:
            # Iniciales como fallback
            iniciales = (u["nombre"][:2] if u and u.get("nombre") else
                         self.usuario[:2]).upper()
            colores = [
                ("#E6F1FB", "#185FA5"), ("#EEEDFE", "#534AB7"),
                ("#E1F5EE", "#0F6E56"), ("#FAEEDA", "#854F0B"),
            ]
            idx = sum(ord(c) for c in self.usuario) % len(colores)
            bg, fg = colores[idx]
            self.lbl_foto.clear()
            self.lbl_foto.setText(iniciales)
            self.lbl_foto.setStyleSheet(f"""
                background:{bg}; color:{fg};
                border-radius:45px;
                font-size:28px; font-weight:bold;
            """)

    def cambiar_foto(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar foto",
            os.path.expanduser("~"),
            "Imágenes (*.png *.jpg *.jpeg *.webp)")
        if path:
            self.um.actualizar_perfil(self.usuario, foto=path)
            u = self.um.buscar(self.usuario)
            self._actualizar_avatar(u)
            QMessageBox.information(self, "✅",
                                    "Foto actualizada. Se verá en el feed la próxima vez que abras la app.")

    def guardar(self):
        nombre = self.inp_nombre.text().strip()
        bio    = self.inp_bio.toPlainText().strip()
        if not nombre:
            QMessageBox.warning(self, "Error", "El nombre no puede estar vacío")
            return
        self.um.actualizar_perfil(self.usuario, nombre=nombre, bio=bio)
        QMessageBox.information(self, "✅", "Perfil actualizado")