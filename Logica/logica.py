from Estructuras.estructuras import Post

class GestorPublicaciones:

    def __init__(self, lista_simple, lista_doble, lista_circular):
        self.lista_simple = lista_simple
        self.lista_doble = lista_doble
        self.lista_circular = lista_circular

        self.modo_circular = False
        self.actual = None

    def crear_publicacion(self, author, content):
        post = Post(author, content)

        self.lista_simple.append(post)
        self.lista_doble.append(post)
        self.lista_circular.append(post)

        if self.actual is None:
            self.actual = self.lista_simple.head

        return post

    def contar_publicaciones(self):
        return self.lista_simple.count()

    def siguiente(self):
        if not self.actual:
            return None

        # MODO CIRCULAR
        if self.modo_circular:
            self.actual = self.actual.siguiente
            return self.actual.data

        # MODO NORMAL
        if self.actual.siguiente:
            self.actual = self.actual.siguiente
            return self.actual.data

        return None

    def anterior(self):
        if not self.actual:
            return None

        # Para lista doble
        if hasattr(self.actual, "anterior") and self.actual.anterior:
            self.actual = self.actual.anterior
            return self.actual.data

        return None

    def obtener_actual(self):
        return self.actual.data if self.actual else None

    def activar_modo_circular(self):
        self.modo_circular = True
        self.actual = self.lista_circular.head

    def desactivar_modo_circular(self):
        self.modo_circular = False
        self.actual = self.lista_simple.head