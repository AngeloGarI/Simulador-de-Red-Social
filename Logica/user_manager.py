import json
import os

class UserManager:
    def __init__(self):
        base = os.path.dirname(os.path.abspath(__file__))
        self.archivo = os.path.join(base, "..", "data", "users.json")
        self.usuarios = []
        self.cargar()

    def cargar(self):
        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                contenido = json.load(f)
            self.usuarios = contenido.get("usuarios", [])
        except FileNotFoundError:
            self.usuarios = []
            self.guardar()

    def guardar(self):
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump({"usuarios": self.usuarios}, f, indent=4, ensure_ascii=False)

    # ── Autenticación ──────────────────────────────────────────
    def login(self, username, password):
        """Retorna el dict del usuario si las credenciales son correctas, si no None."""
        for u in self.usuarios:
            if u["username"] == username and u["password"] == password:
                return u
        return None

    def registrar(self, username, password, nombre=""):
        """Retorna True si se creó, False si el username ya existe."""
        if self.buscar(username):
            return False
        nuevo = {
            "username": username,
            "password": password,
            "nombre": nombre or username,
            "bio": "",
            "foto": "",
            "amigos": [],
            "solicitudes_enviadas": [],
            "solicitudes_recibidas": [],
            "guardados": [],
            "configuracion": {
                "mostrar_en_linea": True,
                "mensajes_desconocidos": True,
                "tema": "claro"
            }
        }
        self.usuarios.append(nuevo)
        self.guardar()
        return True

    # ── Búsqueda ───────────────────────────────────────────────
    def buscar(self, username):
        """Retorna el dict del usuario o None."""
        for u in self.usuarios:
            if u["username"] == username:
                return u
        return None

    def buscar_usuarios(self, keyword):
        """Busca por username o nombre. Retorna lista de dicts."""
        kw = keyword.lower()
        return [u for u in self.usuarios
                if kw in u["username"].lower() or kw in u["nombre"].lower()]

    def get_todos(self):
        return self.usuarios

    # ── Perfil ─────────────────────────────────────────────────
    def actualizar_perfil(self, username, nombre=None, bio=None, foto=None):
        u = self.buscar(username)
        if not u:
            return False
        if nombre is not None:
            u["nombre"] = nombre
        if bio is not None:
            u["bio"] = bio
        if foto is not None:
            u["foto"] = foto
        self.guardar()
        return True

    def cambiar_password(self, username, password_actual, nueva):
        u = self.buscar(username)
        if not u or u["password"] != password_actual:
            return False
        u["password"] = nueva
        self.guardar()
        return True

    # ── Amigos ─────────────────────────────────────────────────
    def enviar_solicitud(self, de, para):
        u_de   = self.buscar(de)
        u_para = self.buscar(para)
        if not u_de or not u_para:
            return False
        if para in u_de["amigos"]:
            return False   # ya son amigos
        if para in u_de["solicitudes_enviadas"]:
            return False   # ya enviada
        u_de["solicitudes_enviadas"].append(para)
        u_para["solicitudes_recibidas"].append(de)
        self.guardar()
        return True

    def aceptar_solicitud(self, usuario, de):
        u        = self.buscar(usuario)
        u_de     = self.buscar(de)
        if not u or not u_de:
            return False
        if de not in u["solicitudes_recibidas"]:
            return False
        u["solicitudes_recibidas"].remove(de)
        u_de["solicitudes_enviadas"].remove(usuario)
        u["amigos"].append(de)
        u_de["amigos"].append(usuario)
        self.guardar()
        return True

    def rechazar_solicitud(self, usuario, de):
        u    = self.buscar(usuario)
        u_de = self.buscar(de)
        if not u or not u_de:
            return False
        if de in u["solicitudes_recibidas"]:
            u["solicitudes_recibidas"].remove(de)
        if usuario in u_de["solicitudes_enviadas"]:
            u_de["solicitudes_enviadas"].remove(usuario)
        self.guardar()
        return True

    def get_amigos(self, username):
        u = self.buscar(username)
        return u["amigos"] if u else []

    def get_solicitudes_recibidas(self, username):
        u = self.buscar(username)
        return u["solicitudes_recibidas"] if u else []

    # ── Guardados ──────────────────────────────────────────────
    def toggle_guardado(self, username, post_id):
        u = self.buscar(username)
        if not u:
            return False
        if post_id in u["guardados"]:
            u["guardados"].remove(post_id)
        else:
            u["guardados"].append(post_id)
        self.guardar()
        return True

    def get_guardados(self, username):
        u = self.buscar(username)
        return u["guardados"] if u else []

    def guardar_config(self, username, config: dict):
        u = self.buscar(username)
        if not u:
            return False
        u["configuracion"].update(config)
        self.guardar()
        return True

    def get_config(self, username):
        u = self.buscar(username)
        return u.get("configuracion", {}) if u else {}

    def guardar_sesion(self, username):
        sesion_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "data", "sesion.json")
        with open(sesion_path, "w", encoding="utf-8") as f:
            json.dump({"usuario": username}, f)

    def cargar_sesion(self):
        sesion_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "data", "sesion.json")
        try:
            with open(sesion_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("usuario")
        except FileNotFoundError:
            return None

    def cerrar_sesion(self):
        sesion_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "data", "sesion.json")
        if os.path.exists(sesion_path):
            os.remove(sesion_path)