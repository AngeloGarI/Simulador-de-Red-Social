import os

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt
from functools import partial
from Logica.social_network import SocialNetwork
from Logica.user_manager import UserManager

class Feed(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.modo_oscuro = False
        self.color_card = "white"
        self.social_network = SocialNetwork()
        self.um = UserManager()
        self.imagen_path = ""

        self.setWindowTitle("Fakebook")
        self.resize(1200, 700)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ── Barra superior ─────────────────────────────────────
        self.barra = QFrame()
        self.barra.setStyleSheet("background:#1877f2;")
        self.barra.setFixedHeight(70)
        barra_layout = QHBoxLayout()
        barra_layout.setContentsMargins(16, 0, 16, 0)

        logo = QLabel("Fakebook")
        logo.setStyleSheet("color:white;")
        logo.setFont(QFont("Arial", 22, QFont.Weight.Bold))

        self.buscar = QLineEdit()
        self.buscar.setPlaceholderText("🔍 Buscar usuarios o posts")
        self.buscar.setFixedWidth(300)
        self.buscar.setStyleSheet(
            "background:white; border-radius:20px; padding:6px 14px; color:black;")
        self.buscar.returnPressed.connect(self.buscar_contenido)

        btn_inicio = QPushButton("🏠 Inicio")
        btn_amigos = QPushButton("👥 Amigos")
        btn_notif = QPushButton("🔔 Notificaciones")
        btn_user = QPushButton(f"👤 {self.usuario}")

        for b in [btn_inicio, btn_amigos, btn_notif, btn_user]:
            b.setStyleSheet("""
                QPushButton { color:white; background:#1877f2; border:none;
                    padding:10px; font-size:14px; }
                QPushButton:hover { background:#166fe5; border-radius:5px; }
            """)

        btn_inicio.clicked.connect(self.cargar_posts)
        btn_amigos.clicked.connect(self.abrir_amigos)
        btn_notif.clicked.connect(self.abrir_notificaciones)
        btn_user.clicked.connect(self.menu_usuario)

        barra_layout.addWidget(logo)
        barra_layout.addSpacing(20)
        barra_layout.addWidget(self.buscar)
        barra_layout.addStretch()
        barra_layout.addWidget(btn_inicio)
        barra_layout.addWidget(btn_amigos)
        barra_layout.addWidget(btn_notif)
        barra_layout.addWidget(btn_user)
        self.barra.setLayout(barra_layout)
        main_layout.addWidget(self.barra)

        # ── Body ───────────────────────────────────────────────
        body = QHBoxLayout()
        body.setContentsMargins(16, 16, 16, 16)
        body.setSpacing(16)
        # Panel izquierdo
        izq = QVBoxLayout()
        izq.setAlignment(Qt.AlignmentFlag.AlignTop)
        info_usuario = self.um.buscar(self.usuario)
        nombre = info_usuario["nombre"] if info_usuario else self.usuario
        bio = info_usuario["bio"] if info_usuario else ""
        foto = info_usuario.get("foto", "") if info_usuario else ""

        # ── Foto de perfil circular ────────────────────────────
        from PyQt6.QtGui import QPainter, QColor, QPainterPath

        lbl_avatar = QLabel()
        lbl_avatar.setFixedSize(64, 64)
        lbl_avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if foto and os.path.exists(foto):
            from PyQt6.QtGui import QPixmap
            resultado = QPixmap(64, 64)
            resultado.fill(QColor(0, 0, 0, 0))
            original = QPixmap(foto).scaled(
                64, 64,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation)
            x = (original.width() - 64) // 2
            y = (original.height() - 64) // 2
            original = original.copy(x, y, 64, 64)
            painter = QPainter(resultado)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            path = QPainterPath()
            path.addEllipse(0, 0, 64, 64)
            painter.setClipPath(path)
            painter.drawPixmap(0, 0, original)
            painter.end()
            lbl_avatar.setPixmap(resultado)
            lbl_avatar.setStyleSheet("background:transparent;")
        else:
            iniciales = nombre[:2].upper()
            colores_avatar = [
                ("#E6F1FB", "#185FA5"), ("#EEEDFE", "#534AB7"),
                ("#E1F5EE", "#0F6E56"), ("#FAEEDA", "#854F0B"),
            ]
            idx = sum(ord(c) for c in self.usuario) % len(colores_avatar)
            bg_av, fg_av = colores_avatar[idx]
            lbl_avatar.setText(iniciales)
            lbl_avatar.setStyleSheet(f"""
                background:{bg_av}; color:{fg_av};
                border-radius:32px;
                font-size:20px; font-weight:bold;
            """)

        # Centrar avatar
        avatar_row = QHBoxLayout()
        avatar_row.addStretch()
        avatar_row.addWidget(lbl_avatar)
        avatar_row.addStretch()

        # Nombre y bio
        lbl_nombre = QLabel(nombre)
        lbl_nombre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_nombre.setStyleSheet("font-weight:bold; font-size:15px;")
        lbl_bio = QLabel(bio or "Sin bio")
        lbl_bio.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_bio.setStyleSheet("color:gray; font-size:12px;")
        lbl_bio.setWordWrap(True)

        # Separador
        sep_izq = QFrame()
        sep_izq.setFrameShape(QFrame.Shape.HLine)
        sep_izq.setStyleSheet("color:#e4e6eb; margin:4px 0;")

        # Botones de navegación
        btn_perfil = QPushButton("👤 Mi perfil")
        btn_guardados = QPushButton("💾 Guardados")
        btn_amigos_l = QPushButton("👥 Amigos")

        for b in [btn_perfil, btn_guardados, btn_amigos_l]:
            b.setStyleSheet("""
                QPushButton { text-align:left; padding:8px 12px;
                    border:none; border-radius:8px; font-size:14px; }
                QPushButton:hover { background:#e4e6eb; }
            """)

        btn_perfil.clicked.connect(self.abrir_perfil)
        btn_guardados.clicked.connect(self.ver_guardados)
        btn_amigos_l.clicked.connect(self.abrir_amigos)

        izq.addLayout(avatar_row)
        izq.addSpacing(6)
        izq.addWidget(lbl_nombre)
        izq.addWidget(lbl_bio)
        izq.addWidget(sep_izq)
        izq.addSpacing(4)
        izq.addWidget(btn_perfil)
        izq.addWidget(btn_guardados)
        izq.addWidget(btn_amigos_l)
        izq.addStretch()
        body.addLayout(izq, 1)

        # Panel central
        centro = QVBoxLayout()

        self.caja = QFrame()
        self.caja.setStyleSheet("background:white; border-radius:10px; padding:10px;")
        pub_layout = QVBoxLayout()

        self.post = QTextEdit()
        self.post.setPlaceholderText("¿Qué estás pensando?")
        self.post.setFixedHeight(80)

        fila_btn = QHBoxLayout()
        self.lbl_imagen_sel = QLabel("Sin imagen")
        self.lbl_imagen_sel.setStyleSheet("color:gray; font-size:12px;")

        btn_imagen = QPushButton("🖼️ Foto")
        btn_imagen.setStyleSheet("""
            QPushButton { background:#e4e6eb; color:#050505;
                border-radius:8px; padding:6px 14px; font-size:13px; border:none; }
            QPushButton:hover { background:#d8dadf; }
        """)
        btn_imagen.clicked.connect(self.seleccionar_imagen)

        btn_publicar = QPushButton("Publicar")
        btn_publicar.setStyleSheet("""
            QPushButton { background:#1877f2; color:white;
                border-radius:8px; padding:8px 20px; font-weight:bold; border:none; }
            QPushButton:hover { background:#166fe5; }
        """)
        btn_publicar.clicked.connect(self.publicar)

        fila_btn.addWidget(btn_imagen)
        fila_btn.addWidget(self.lbl_imagen_sel)
        fila_btn.addStretch()
        fila_btn.addWidget(btn_publicar)

        pub_layout.addWidget(self.post)
        pub_layout.addLayout(fila_btn)
        self.caja.setLayout(pub_layout)
        centro.addWidget(self.caja)

        # Feed con scroll
        self.feed_layout = QVBoxLayout()
        self.feed_layout.setSpacing(10)
        cont = QWidget()
        cont.setLayout(self.feed_layout)
        scroll = QScrollArea()
        scroll.setWidget(cont)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border:none;")
        centro.addWidget(scroll)
        body.addLayout(centro, 3)

        # Panel derecho — contactos
        der = QVBoxLayout()
        der.setAlignment(Qt.AlignmentFlag.AlignTop)
        lbl_contactos = QLabel("Contactos")
        lbl_contactos.setStyleSheet("font-weight:bold; font-size:14px;")
        der.addWidget(lbl_contactos)

        self.lista_online = QListWidget()
        self.lista_online.setStyleSheet("border:none;")
        self._cargar_contactos()
        self.lista_online.itemClicked.connect(self.abrir_chat)
        der.addWidget(self.lista_online)
        der.addStretch()
        body.addLayout(der, 1)

        main_layout.addLayout(body)
        self.setLayout(main_layout)

        self.aplicar_tema()
        self.cargar_posts()

    def aplicar_tema(self):
        if self.modo_oscuro:
            self.setStyleSheet("QWidget{background:#18191a; color:white;}")
            self.color_card = "#242526"
        else:
            self.setStyleSheet("QWidget{background:#f0f2f5; color:black;}")
            self.color_card = "white"
        self.caja.setStyleSheet(
            f"background:{self.color_card}; border-radius:10px; padding:10px;")

    def _cargar_contactos(self):
        self.lista_online.clear()
        amigos = self.um.get_amigos(self.usuario)
        if amigos:
            for a in amigos:
                self.lista_online.addItem(f"🟢 {a}")
        else:
            self.lista_online.addItem("Sin amigos aún")

    def publicar(self):
        texto = self.post.toPlainText().strip()
        if not texto:
            return
        self.social_network.create_post(self.usuario, texto)
        self.post.clear()
        self.cargar_posts()

    def cargar_posts(self):
        self._limpiar_feed()
        for post in reversed(self.social_network.get_feed()):
            self.feed_layout.addWidget(self.crear_card_post(post))

    def _limpiar_feed(self):
        for i in reversed(range(self.feed_layout.count())):
            w = self.feed_layout.itemAt(i).widget()
            if w:
                w.deleteLater()

    def crear_card_post(self, post):
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background:{self.color_card};
                border-radius:12px;
                border:1px solid {"#3a3b3c" if self.modo_oscuro else "#e4e6eb"};
            }}
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        color = "white" if self.modo_oscuro else "#050505"
        color_muted = "#b0b3b8" if self.modo_oscuro else "#65676b"
        bg_hover = "#3a3b3c" if self.modo_oscuro else "#f0f2f5"
        es_dueno = (post.author == self.usuario)
        guardados = self.um.get_guardados(self.usuario)
        esta_guardado = post.id in guardados

        # ── Header (avatar + nombre + hora) ───────────────────────
        header = QHBoxLayout()
        header.setContentsMargins(14, 12, 14, 8)
        header.setSpacing(10)

        # Avatar circular con iniciales
        iniciales = post.author[:2].upper()
        colores_avatar = [
            ("#E6F1FB", "#185FA5"), ("#EEEDFE", "#534AB7"),
            ("#E1F5EE", "#0F6E56"), ("#FAEEDA", "#854F0B"),
            ("#FAECE7", "#993C1D"), ("#F4C0D1", "#72243E"),
        ]
        idx = sum(ord(c) for c in post.author) % len(colores_avatar)
        bg_av, fg_av = colores_avatar[idx]

        avatar = QLabel(iniciales)
        avatar.setFixedSize(42, 42)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet(f"""
            QLabel {{
                background:{bg_av};
                color:{fg_av};
                border-radius:21px;
                font-weight:600;
                font-size:14px;
            }}
        """)

        meta = QVBoxLayout()
        meta.setSpacing(1)
        lbl_autor = QPushButton(post.author)
        lbl_autor.setStyleSheet(f"""
            QPushButton {{ color:{color}; font-weight:600; font-size:14px;
                background:transparent; border:none; padding:0; text-align:left; }}
            QPushButton:hover {{ text-decoration:underline; color:#1877f2; }}
        """)
        lbl_autor.clicked.connect(partial(self.ver_perfil_usuario, post.author))
        lbl_hora = QLabel(post.timestamp)
        lbl_hora.setStyleSheet(f"color:{color_muted}; font-size:12px;")
        meta.addWidget(lbl_autor)
        meta.addWidget(lbl_hora)

        header.addWidget(avatar)
        header.addLayout(meta)
        header.addStretch()

        # Menú editar/eliminar solo al dueño
        if es_dueno:
            btn_menu = QPushButton("•••")
            btn_menu.setFixedSize(32, 32)
            btn_menu.setStyleSheet(f"""
                QPushButton {{
                    color:{color_muted}; background:transparent;
                    border:none; border-radius:16px; font-size:14px;
                }}
                QPushButton:hover {{ background:{bg_hover}; }}
            """)
            btn_menu.clicked.connect(partial(self._menu_post, post))
            header.addWidget(btn_menu)

        header_w = QWidget()
        header_w.setLayout(header)
        header_w.setStyleSheet("background:transparent;")
        layout.addWidget(header_w)

        # ── Contenido ──────────────────────────────────────────────
        lbl_texto = QLabel(post.content)
        lbl_texto.setStyleSheet(f"""
            color:{color}; font-size:14px;
            padding:0 14px 12px 14px;
            background:transparent;
        """)
        lbl_texto.setWordWrap(True)
        layout.addWidget(lbl_texto)

        # Imagen del post si existe
        if hasattr(post, 'imagen') and post.imagen and os.path.exists(post.imagen):
            lbl_img = QLabel()
            pix = QPixmap(post.imagen).scaledToWidth(
                500, Qt.TransformationMode.SmoothTransformation)
            lbl_img.setPixmap(pix)
            lbl_img.setStyleSheet("padding:0 14px 10px 14px; background:transparent;")
            lbl_img.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(lbl_img)

        # ── Separador ──────────────────────────────────────────────
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color:{'#3a3b3c' if self.modo_oscuro else '#e4e6eb'}; background:transparent;")
        layout.addWidget(sep)

        # ── Botones de acción ──────────────────────────────────────
        acciones = QHBoxLayout()
        acciones.setContentsMargins(8, 2, 8, 2)
        acciones.setSpacing(2)

        estilo_accion = f"""
            QPushButton {{
                background:transparent; color:{color_muted};
                border:none; border-radius:8px;
                padding:8px 4px; font-size:13px; font-weight:500;
            }}
            QPushButton:hover {{ background:{bg_hover}; color:{color}; }}
        """
        estilo_guardado = f"""
            QPushButton {{
                background:transparent; color:#0F6E56;
                border:none; border-radius:8px;
                padding:8px 4px; font-size:13px; font-weight:500;
            }}
            QPushButton:hover {{ background:{bg_hover}; }}
        """

        btn_like = QPushButton(f"👍  Me gusta · {post.likes}")
        btn_dislike = QPushButton(f"👎  No me gusta · {post.dislikes}")
        btn_guardar = QPushButton("🔖  Guardado" if esta_guardado else "🔖  Guardar")
        btn_comment = QPushButton("💬  Comentar")

        for b in [btn_like, btn_dislike, btn_comment]:
            b.setStyleSheet(estilo_accion)
        btn_guardar.setStyleSheet(estilo_guardado if esta_guardado else estilo_accion)

        btn_like.clicked.connect(partial(self.like, post))
        btn_dislike.clicked.connect(partial(self.dislike, post))
        btn_guardar.clicked.connect(partial(self.toggle_guardar, post))
        btn_comment.clicked.connect(partial(self._toggle_comentarios, post, card))

        for b in [btn_like, btn_dislike, btn_guardar, btn_comment]:
            b.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            acciones.addWidget(b)

        acciones_w = QWidget()
        acciones_w.setLayout(acciones)
        acciones_w.setStyleSheet("background:transparent;")
        layout.addWidget(acciones_w)

        # ── Sección comentarios (oculta inicialmente) ──────────────
        self._agregar_seccion_comentarios(post, layout, color, color_muted, bg_hover)

        card.setLayout(layout)
        return card

    def _menu_post(self, post):
        """Menú contextual editar/eliminar para el dueño."""
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu { border-radius:8px; padding:4px; }
            QMenu::item { padding:8px 20px; border-radius:6px; }
            QMenu::item:selected { background:#e4e6eb; }
        """)
        act_editar = menu.addAction("✏️  Editar")
        act_eliminar = menu.addAction("🗑  Eliminar")
        accion = menu.exec(self.cursor().pos())
        if accion == act_editar:
            self.editar_post(post)
        elif accion == act_eliminar:
            self.eliminar_post(post)

    def _agregar_seccion_comentarios(self, post, layout, color, color_muted, bg_hover):
        """Sección de comentarios colapsable."""
        contenedor = QWidget()
        contenedor.setStyleSheet("background:transparent;")
        contenedor.setVisible(False)
        vbox = QVBoxLayout()
        vbox.setContentsMargins(14, 8, 14, 12)
        vbox.setSpacing(8)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color:{'#3a3b3c' if self.modo_oscuro else '#e4e6eb'};")
        vbox.addWidget(sep)

        # Comentarios existentes
        for c in post.comments:
            self._agregar_burbuja(vbox, c, color, color_muted)

        # Campo nuevo comentario
        fila = QHBoxLayout()
        inp = QLineEdit()
        inp.setPlaceholderText("Escribe un comentario...")
        inp.setStyleSheet(f"""
            QLineEdit {{
                background:{"#3a3b3c" if self.modo_oscuro else "#f0f2f5"};
                border:none; border-radius:20px;
                padding:8px 14px; font-size:13px; color:{color};
            }}
        """)
        btn_env = QPushButton("➤")
        btn_env.setFixedSize(36, 36)
        btn_env.setStyleSheet("""
            QPushButton { background:#1877f2; color:white;
                border-radius:18px; font-size:14px; border:none; }
            QPushButton:hover { background:#166fe5; }
        """)

        def enviar_comentario():
            texto = inp.text().strip()
            if not texto:
                return
            comentario = f"{self.usuario}: {texto}"
            self.social_network.add_comment(post, comentario)
            self._agregar_burbuja(vbox, comentario, color, color_muted, antes_de=fila_w)
            inp.clear()

        btn_env.clicked.connect(enviar_comentario)
        inp.returnPressed.connect(enviar_comentario)

        fila.addWidget(inp)
        fila.addWidget(btn_env)
        fila_w = QWidget()
        fila_w.setLayout(fila)
        fila_w.setStyleSheet("background:transparent;")
        vbox.addWidget(fila_w)

        contenedor.setLayout(vbox)
        layout.addWidget(contenedor)

        # Guardar referencia para toggle
        if not hasattr(self, '_comment_containers'):
            self._comment_containers = {}
        self._comment_containers[post.id] = contenedor

    def _agregar_burbuja(self, layout, texto, color, color_muted, antes_de=None):
        """Agrega una burbuja de comentario al layout."""
        partes = texto.split(": ", 1)
        autor = partes[0] if len(partes) == 2 else "?"
        mensaje = partes[1] if len(partes) == 2 else texto
        iniciales = autor[:2].upper()

        colores_avatar = [
            ("#E6F1FB", "#185FA5"), ("#EEEDFE", "#534AB7"),
            ("#E1F5EE", "#0F6E56"), ("#FAEEDA", "#854F0B"),
        ]
        idx = sum(ord(c) for c in autor) % len(colores_avatar)
        bg_av, fg_av = colores_avatar[idx]

        fila = QHBoxLayout()
        fila.setSpacing(8)
        fila.setContentsMargins(0, 0, 0, 0)

        av = QLabel(iniciales)
        av.setFixedSize(30, 30)
        av.setAlignment(Qt.AlignmentFlag.AlignCenter)
        av.setStyleSheet(f"""
            background:{bg_av}; color:{fg_av};
            border-radius:15px; font-size:11px; font-weight:600;
        """)

        burbuja = QWidget()
        burbuja.setStyleSheet(f"""
            background:{"#3a3b3c" if self.modo_oscuro else "#f0f2f5"};
            border-radius:0 12px 12px 12px;
        """)
        b_layout = QVBoxLayout()
        b_layout.setContentsMargins(10, 6, 10, 6)
        b_layout.setSpacing(2)
        lbl_autor = QLabel(autor)
        lbl_autor.setStyleSheet(f"color:{color}; font-weight:600; font-size:12px; background:transparent;")
        lbl_msg = QLabel(mensaje)
        lbl_msg.setStyleSheet(f"color:{color}; font-size:13px; background:transparent;")
        lbl_msg.setWordWrap(True)
        b_layout.addWidget(lbl_autor)
        b_layout.addWidget(lbl_msg)
        burbuja.setLayout(b_layout)

        fila.addWidget(av, 0, Qt.AlignmentFlag.AlignTop)
        fila.addWidget(burbuja, 1)

        w = QWidget()
        w.setLayout(fila)
        w.setStyleSheet("background:transparent;")

        if antes_de:
            idx = layout.indexOf(antes_de)
            layout.insertWidget(idx, w)
        else:
            layout.addWidget(w)

    def _toggle_comentarios(self, post, card):
        """Muestra u oculta la sección de comentarios."""
        if not hasattr(self, '_comment_containers'):
            return
        contenedor = self._comment_containers.get(post.id)
        if contenedor:
            contenedor.setVisible(not contenedor.isVisible())

    def like(self, post):
        self.social_network.add_like(post)
        self.cargar_posts()

    def dislike(self, post):
        self.social_network.add_dislike(post)
        self.cargar_posts()

    def toggle_guardar(self, post):
        self.um.toggle_guardado(self.usuario, post.id)
        self.cargar_posts()

    def editar_post(self, post):
        nuevo, ok = QInputDialog.getText(
            self, "Editar publicación", "Nuevo texto:", text=post.content)
        if ok and nuevo.strip():
            post.content = nuevo.strip()
            self.social_network.guardar_datos()
            self.cargar_posts()

    def eliminar_post(self, post):
        confirm = QMessageBox.question(
            self, "Eliminar", "¿Eliminar esta publicación?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            self.social_network.delete_post(post)
            self.cargar_posts()

    def buscar_contenido(self):
        keyword = self.buscar.text().strip()
        if not keyword:
            self.cargar_posts()
            return

        self._limpiar_feed()

        # Buscar posts
        posts = self.social_network.search_posts(keyword)
        if posts:
            lbl = QLabel(f"📄 Posts con '{keyword}':")
            lbl.setStyleSheet("font-weight:bold; padding:4px;")
            self.feed_layout.addWidget(lbl)
            for p in posts:
                self.feed_layout.addWidget(self.crear_card_post(p))

        # Buscar usuarios
        usuarios = self.um.buscar_usuarios(keyword)
        if usuarios:
            lbl2 = QLabel(f"👤 Usuarios con '{keyword}':")
            lbl2.setStyleSheet("font-weight:bold; padding:4px; margin-top:8px;")
            self.feed_layout.addWidget(lbl2)
            for u in usuarios:
                card = self._crear_card_usuario(u)
                self.feed_layout.addWidget(card)

        if not posts and not usuarios:
            lbl_vacio = QLabel("Sin resultados.")
            lbl_vacio.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.feed_layout.addWidget(lbl_vacio)

    def _crear_card_usuario(self, u):
        card = QFrame()
        card.setStyleSheet(
            f"background:{self.color_card}; border-radius:10px; padding:10px;")
        layout = QHBoxLayout()
        info = QVBoxLayout()
        info.addWidget(QLabel(f"👤 {u['nombre']} (@{u['username']})"))
        bio_lbl = QLabel(u.get("bio", "") or "Sin bio")
        bio_lbl.setStyleSheet("color:gray; font-size:12px;")
        info.addWidget(bio_lbl)

        amigos = self.um.get_amigos(self.usuario)
        enviadas = self.um.buscar(self.usuario)
        enviadas = enviadas["solicitudes_enviadas"] if enviadas else []

        if u["username"] != self.usuario:
            if u["username"] in amigos:
                btn = QPushButton("✅ Amigos")
                btn.setEnabled(False)
            elif u["username"] in enviadas:
                btn = QPushButton("⏳ Solicitud enviada")
                btn.setEnabled(False)
            else:
                btn = QPushButton("➕ Agregar amigo")
                btn.clicked.connect(partial(self.enviar_solicitud, u["username"]))
            layout.addLayout(info)
            layout.addWidget(btn)
        else:
            layout.addLayout(info)

        card.setLayout(layout)
        return card

    def enviar_solicitud(self, para):
        if self.um.enviar_solicitud(self.usuario, para):
            QMessageBox.information(self, "✅", f"Solicitud enviada a {para}")
            self.buscar_contenido()
        else:
            QMessageBox.warning(self, "Error", "No se pudo enviar la solicitud")

    def abrir_perfil(self):
        from Interfaz.ui_perfil import Perfil
        self.perfil_window = Perfil(self.usuario, self.um)
        self.perfil_window.show()

    def ver_guardados(self):
        ids = self.um.get_guardados(self.usuario)
        todos = self.social_network.get_feed()
        guardados = [p for p in todos if p.id in ids]

        win = QWidget()
        win.setWindowTitle("💾 Guardados")
        win.resize(500, 500)
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Tienes {len(guardados)} publicaciones guardadas"))
        for p in guardados:
            layout.addWidget(self.crear_card_post(p))
        win.setLayout(layout)
        self.guardados_window = win
        win.show()

    def abrir_amigos(self):
        from Interfaz.ui_amigos import Amigos
        self.amigos_window = Amigos(self.usuario, self.um)
        self.amigos_window.show()

    def abrir_notificaciones(self):
        from Interfaz.ui_notificaciones import Notificaciones
        self.not_window = Notificaciones(self.usuario, self.um)
        self.not_window.show()

    def abrir_chat(self, item):
        nombre = item.text().replace("🟢 ", "").strip()
        if nombre == "Sin amigos aún":
            return
        from ui_chat import Chat
        self.chat_window = Chat(self.usuario, nombre)
        self.chat_window.show()

    def menu_usuario(self):
        menu = QMenu(self)
        bg    = "#242526" if self.modo_oscuro else "white"
        color = "white"   if self.modo_oscuro else "black"
        hover = "#3a3b3c" if self.modo_oscuro else "#e4e6eb"
        menu.setStyleSheet(f"""
            QMenu {{ background:{bg}; color:{color};
                border-radius:10px; padding:5px; }}
            QMenu::item {{ padding:8px 25px; border-radius:5px; }}
            QMenu::item:selected {{ background:{hover}; }}
        """)

        act_perfil = menu.addAction("👤 Mi perfil")
        act_config = menu.addAction("⚙️ Configuración")
        act_ayuda  = menu.addAction("❓ Soporte técnico")
        menu.addSeparator()
        tema_menu  = QMenu("🌙 Tema", self)
        act_claro  = tema_menu.addAction("Modo claro")
        act_oscuro = tema_menu.addAction("Modo oscuro")
        menu.addMenu(tema_menu)
        menu.addSeparator()
        act_cerrar = menu.addAction("🚪 Cerrar sesión")

        boton = self.sender()
        pos = boton.mapToGlobal(boton.rect().bottomLeft())
        pos.setX(pos.x() - 120)
        pos.setY(pos.y() + 5)
        accion = menu.exec(pos)

        if accion == act_perfil:
            self.abrir_perfil()
        elif accion == act_config:
            from Interfaz.ui_configuracion import Configuracion
            self.config_window = Configuracion(self.usuario, self.um)
            self.config_window.show()
        elif accion == act_ayuda:
            from Interfaz.ui_ayuda import Ayuda
            self.ayuda_window = Ayuda()
            self.ayuda_window.show()
        elif accion == act_claro:
            self.modo_oscuro = False
            self.aplicar_tema()
            self.cargar_posts()
        elif accion == act_oscuro:
            self.modo_oscuro = True
            self.aplicar_tema()
            self.cargar_posts()
        elif accion == act_cerrar:
            self.um.cerrar_sesion()
            from Interfaz.ui_login import Login
            self.login_window = Login()
            self.login_window.show()
            self.close()

    def seleccionar_imagen(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar imagen",
            os.path.expanduser("~"),
            "Imágenes (*.png *.jpg *.jpeg *.webp)")
        if path:
            self.imagen_path = path
            nombre = os.path.basename(path)
            self.lbl_imagen_sel.setText(f"📎 {nombre}")

    def publicar(self):
        texto = self.post.toPlainText().strip()
        if not texto and not self.imagen_path:
            return
        post = self.social_network.create_post(
            self.usuario, texto or "📷 Imagen")
        if self.imagen_path:
            post.imagen = self.imagen_path
            self.social_network.guardar_datos()
        self.imagen_path = ""
        self.lbl_imagen_sel.setText("Sin imagen")
        self.post.clear()
        self.cargar_posts()

    def ver_perfil_usuario(self, username):
        from Interfaz.ui_perfil import Perfil
        es_propio = (username == self.usuario)
        self.perfil_ext = Perfil(username, self.um,
                                 solo_lectura=not es_propio)
        self.perfil_ext.show()

    def refrescar_panel_izquierdo(self):
        """Llamar después de cambiar foto de perfil."""
        # Simplemente recarga la ventana completa del feed
        nueva = Feed(self.usuario)
        nueva.show()
        self.close()