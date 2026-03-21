from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from datetime import datetime
from database import cursor,conn
from functools import partial

class Feed(QWidget):


    def __init__(self,usuario):

        super().__init__()

        self.usuario = usuario
        self.modo_oscuro = False
        self.color_card = "white"

        self.setWindowTitle("Fakebook")
        self.resize(1200,700)

        main_layout = QVBoxLayout()


        self.barra = QFrame()
        self.barra.setStyleSheet("background:#1877f2;")
        self.barra.setFixedHeight(70)

        barra_layout = QHBoxLayout()

        logo = QLabel("Fakebook")
        logo.setStyleSheet("color:white;")
        logo.setFont(QFont("Arial",22,QFont.Weight.Bold))

        buscar = QLineEdit()
        buscar.setPlaceholderText("🔍 Buscar en Fakebook")
        buscar.setFixedWidth(300)

        btn_inicio = QPushButton("🏠 Inicio")
        btn_amigos = QPushButton("👥 Amigos")
        btn_notif = QPushButton("🔔 Notificaciones")
        btn_user = QPushButton(self.usuario)

        for b in [btn_inicio,btn_amigos,btn_notif,btn_user]:
            b.setStyleSheet("""
            QPushButton{
                color:white;
                background:#1877f2;
                border:none;
                padding:10px;
                font-size:14px;
            }
            QPushButton:hover{
                background:#166fe5;
                border-radius:5px;
            }
            """)

        btn_amigos.clicked.connect(self.abrir_amigos)
        btn_notif.clicked.connect(self.abrir_not)
        btn_user.clicked.connect(self.menu_usuario)

        barra_layout.addWidget(logo)
        barra_layout.addSpacing(20)
        barra_layout.addWidget(buscar)
        barra_layout.addStretch()
        barra_layout.addWidget(btn_inicio)
        barra_layout.addWidget(btn_amigos)
        barra_layout.addWidget(btn_notif)
        barra_layout.addWidget(btn_user)

        self.barra.setLayout(barra_layout)
        main_layout.addWidget(self.barra)


        body = QHBoxLayout()

        izquierda = QVBoxLayout()
        izquierda.addWidget(QLabel("👤 "+self.usuario))
        izquierda.addWidget(QLabel("👥 Amigos"))
        izquierda.addWidget(QLabel("🕒 Recuerdos"))
        izquierda.addWidget(QLabel("💾 Guardado"))

        body.addLayout(izquierda,1)


        centro = QVBoxLayout()

        self.caja = QFrame()
        pub_layout = QVBoxLayout()

        self.post = QTextEdit()
        self.post.setPlaceholderText("¿Qué estás pensando?")

        btn_publicar = QPushButton("Publicar")
        btn_publicar.clicked.connect(self.publicar)

        pub_layout.addWidget(self.post)
        pub_layout.addWidget(btn_publicar)

        self.caja.setLayout(pub_layout)
        centro.addWidget(self.caja)

        self.feed = QVBoxLayout()

        cont = QWidget()
        cont.setLayout(self.feed)

        scroll = QScrollArea()
        scroll.setWidget(cont)
        scroll.setWidgetResizable(True)

        centro.addWidget(scroll)

        body.addLayout(centro,3)


        derecha = QVBoxLayout()
        derecha.addWidget(QLabel("Contactos"))

        self.lista_online = QListWidget()
        self.lista_online.addItem("🟢 Carlos")
        self.lista_online.addItem("🟢 Ana")
        self.lista_online.addItem("🟢 Luis")

        self.lista_online.itemClicked.connect(self.abrir_chat)

        derecha.addWidget(self.lista_online)

        body.addLayout(derecha,1)

        main_layout.addLayout(body)
        self.setLayout(main_layout)

        self.aplicar_tema()
        self.cargar_posts()


    def aplicar_tema(self):

        if self.modo_oscuro:
            self.setStyleSheet("QWidget{background:#18191a;color:white;}")
            self.color_card = "#242526"
        else:
            self.setStyleSheet("QWidget{background:#f0f2f5;color:black;}")
            self.color_card = "white"

        self.caja.setStyleSheet(f"background:{self.color_card}; border-radius:10px; padding:10px;")


    def publicar(self):

        texto = self.post.toPlainText()
        if texto == "":
            return

        fecha = datetime.now().strftime("%d/%m %H:%M")

        cursor.execute(
        "INSERT INTO publicaciones(usuario,contenido,fecha) VALUES (?,?,?)",
        (self.usuario,texto,fecha)
        )

        conn.commit()

        self.post.clear()
        self.cargar_posts()


    def cargar_posts(self):

        for i in reversed(range(self.feed.count())):
            self.feed.itemAt(i).widget().deleteLater()

        cursor.execute("SELECT * FROM publicaciones ORDER BY id DESC")

        for id,user,texto,fecha in cursor.fetchall():

            card = QFrame()
            card.setStyleSheet(f"background:{self.color_card}; border-radius:10px; padding:10px;")

            layout = QVBoxLayout()

            color_texto = "white" if self.modo_oscuro else "black"

            lbl_user = QLabel(f"{user} • {fecha}")
            lbl_texto = QLabel(texto)

            lbl_user.setStyleSheet(f"color:{color_texto}; font-weight:bold;")
            lbl_texto.setStyleSheet(f"color:{color_texto};")

            layout.addWidget(lbl_user)
            layout.addWidget(lbl_texto)


            cursor.execute("SELECT COUNT(*) FROM likes WHERE post_id=?", (id,))
            likes = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM dislikes WHERE post_id=?", (id,))
            dislikes = cursor.fetchone()[0]

            botones = QHBoxLayout()

            btn_like = QPushButton(f"👍 Me gusta {likes}")
            btn_dislike = QPushButton(f"👎 No me gusta {dislikes}")
            btn_editar = QPushButton("✏️ Editar publicación")
            btn_eliminar = QPushButton("🗑 Eliminar publicación")

            for b in [btn_like, btn_dislike, btn_editar, btn_eliminar]:
                b.setStyleSheet(f"""
                QPushButton {{
                    background:{self.color_card};
                    color:{color_texto};
                    border:1px solid gray;
                    padding:5px;
                    border-radius:5px;
                }}
                QPushButton:hover {{
                    background:#1877f2;
                    color:white;
                }}
                """)

            btn_like.clicked.connect(partial(self.like, id))
            btn_dislike.clicked.connect(partial(self.dislike, id))
            btn_editar.clicked.connect(partial(self.editar_post, id))
            btn_eliminar.clicked.connect(partial(self.eliminar_post, id))

            botones.addWidget(btn_like)
            botones.addWidget(btn_dislike)
            botones.addWidget(btn_editar)
            botones.addWidget(btn_eliminar)

            layout.addLayout(botones)
            card.setLayout(layout)

            self.feed.addWidget(card)



    def like(self, id):
        cursor.execute("INSERT INTO likes(usuario,post_id) VALUES (?,?)",(self.usuario,id))
        conn.commit()
        self.cargar_posts()

    def dislike(self, id):
        cursor.execute("INSERT INTO dislikes(usuario,post_id) VALUES (?,?)",(self.usuario,id))
        conn.commit()
        self.cargar_posts()

    def editar_post(self, id):
        nuevo, ok = QInputDialog.getText(self, "Editar publicación", "Nuevo texto:")
        if ok and nuevo != "":
            cursor.execute("UPDATE publicaciones SET contenido=? WHERE id=?", (nuevo, id))
            conn.commit()
            self.cargar_posts()

    def eliminar_post(self, id):
        cursor.execute("DELETE FROM publicaciones WHERE id=?", (id,))
        conn.commit()
        self.cargar_posts()

    def menu_usuario(self):

        menu = QMenu(self)

        if self.modo_oscuro:
            bg = "#242526"
            color = "white"
            hover = "#3a3b3c"
        else:
            bg = "white"
            color = "black"
            hover = "#e4e6eb"

        menu.setStyleSheet(f"""
        QMenu {{
            background:{bg};
            color:{color};
            border-radius:10px;
            padding:5px;
        }}
        QMenu::item {{
            padding:8px 25px;
            border-radius:5px;
        }}
        QMenu::item:selected {{
            background:{hover};
        }}
        """)

        config = menu.addAction("⚙️ Configuración")
        ayuda = menu.addAction("❓ Soporte técnico")

        tema = QMenu("🌙 Tema", self)
        claro = tema.addAction("Modo claro")
        oscuro = tema.addAction("Modo oscuro")
        menu.addMenu(tema)

        cerrar = menu.addAction("🚪 Cerrar sesión")

        boton = self.sender()
        pos = boton.mapToGlobal(boton.rect().bottomLeft())

        pos.setX(pos.x() - 120)
        pos.setY(pos.y() + 5)

        accion = menu.exec(pos)

        if accion == config:
            QMessageBox.information(self,"Configuración","Aquí puedes configurar tu cuenta.")

        elif accion == claro:
            self.modo_oscuro = False
            self.aplicar_tema()
            self.cargar_posts()

        elif accion == oscuro:
            self.modo_oscuro = True
            self.aplicar_tema()
            self.cargar_posts()

        elif accion == ayuda:
            QMessageBox.information(
                self,
                "Soporte técnico",
                "Para recibir ayuda contacta:\n4560-7604 / 4958-0201 / 3067-8267"
            )

        elif accion == cerrar:
            from ui_login import Login
            self.close()
            self.login = Login()
            self.login.show()


    def abrir_amigos(self):
        from ui_amigos import Amigos
        self.amigos_window = Amigos(self.usuario)
        self.amigos_window.show()

    def abrir_not(self):
        from ui_notificaciones import Notificaciones
        self.not_window = Notificaciones(self.usuario)
        self.not_window.show()

    def abrir_chat(self,item):
        from ui_chat import Chat
        nombre = item.text().replace("🟢 ","")
        self.chat_window = Chat(self.usuario,nombre)
        self.chat_window.show()

