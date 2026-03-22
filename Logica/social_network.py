import json
import os

from Estructuras.estructuras import (
    Post,
    LinkedListSimple,
    LinkedListDoubly,
    LinkedListCircular
)

class SocialNetwork:
    def __init__(self):
        self.lista_simple   = LinkedListSimple()
        self.lista_doble    = LinkedListDoubly()
        self.lista_circular = LinkedListCircular()
        self.modo_circular  = False

        base = os.path.dirname(os.path.abspath(__file__))
        self.archivo = os.path.join(base, "..", "data", "posts.json")

        self.cargar_datos()

    # ── Persistencia ───────────────────────────────────────────
    def guardar_datos(self):
        data = [post.to_dict() for post in self.lista_simple.get_all()]
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump({"posts": data}, f, indent=4, ensure_ascii=False)

    def cargar_datos(self):
        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                contenido = json.load(f)

            items = contenido.get("posts", []) if isinstance(contenido, dict) else contenido

            for item in items:
                if not isinstance(item, dict):
                    continue
                post = Post.from_dict(item)
                self.lista_simple.append(post)
                self.lista_doble.append(post)
                self.lista_circular.append(post)

        except FileNotFoundError:
            os.makedirs(os.path.dirname(self.archivo), exist_ok=True)
            with open(self.archivo, "w", encoding="utf-8") as f:
                json.dump({"posts": []}, f, indent=4)
        except json.JSONDecodeError:
            print("⚠️ posts.json corrupto, iniciando vacío")

    def create_post(self, author, content):
        post = Post(author, content)
        self.lista_simple.append(post)
        self.lista_doble.append(post)
        self.lista_circular.append(post)
        self.guardar_datos()
        return post

    def get_feed(self):
        return self.lista_simple.get_all()

    def add_like(self, post):
        post.likes += 1
        self.guardar_datos()
        return post.likes

    def add_dislike(self, post):
        post.dislikes += 1
        self.guardar_datos()
        return post.dislikes

    def delete_post(self, post):
        self.lista_simple.delete(post)
        self._reconstruir_listas()
        self.guardar_datos()

    def search_posts(self, keyword):
        return self.lista_simple.search(keyword)

    def count_posts(self):
        return self.lista_simple.count()

    def toggle_favorite(self, post):
        post.is_favorite = not post.is_favorite
        self.guardar_datos()

    def add_comment(self, post, comment):
        post.comments.append(comment)
        self.guardar_datos()

    def get_top_posts(self, n=3):
        posts = self.lista_simple.get_all()
        posts.sort(key=lambda p: p.likes, reverse=True)
        return posts[:n]

    def toggle_circular_mode(self):
        self.modo_circular = not self.modo_circular

    def next_post(self):
        if self.modo_circular:
            return self.lista_circular.next_post()
        return self.lista_doble.next_post()

    def prev_post(self):
        return self.lista_doble.prev_post()

    def get_current(self):
        if self.modo_circular:
            return self.lista_circular.get_current()
        return self.lista_doble.get_current()

    def _reconstruir_listas(self):
        posts = self.lista_simple.get_all()
        self.lista_doble    = LinkedListDoubly()
        self.lista_circular = LinkedListCircular()
        for p in posts:
            self.lista_doble.append(p)
            self.lista_circular.append(p)