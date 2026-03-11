"""
Parte 1: estructura de datos
SIMULADOR DE RED SOCIAL
"""

from datetime import datetime

class Post:
    """Representa un post en la red social"""
    _id_counter = 1

    def __init__(self, author: str, content: str):
        self.id = Post._id_counter
        Post._id_counter += 1

        self.author = author
        self.content = content
        self.timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.likes = 0
        self.comments = []
        self.is_favorite = False

    def to_dict(self)->dict:
        return {
            "id": self.id,
            "author": self.author,
            "content": self.content,
            "timestamp": self.timestamp,
            "likes": self.likes,
            "comments": self.comments,
            "is_favorite": self.is_favorite
        }
    @staticmethod
    def from_dict(data: dict):
        post = Post(data["author"], data["content"])
        post.id = data["id"]
        post.timestamp = data["timestamp"]
        post.likes = data["likes"]
        post.comments = data["comments"]
        post.is_favorite = data["is_favorite"]
        return post

    def __str__(self):
        return f"Post #{self.id} by {self.author}: {self.content[:30]}"