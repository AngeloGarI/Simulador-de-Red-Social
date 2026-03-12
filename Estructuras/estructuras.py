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
        if data["id"] >= Post._id_counter:
            Post._id_counter = data["id"] + 1
        post.timestamp = data["timestamp"]
        post.likes = data["likes"]
        post.comments = data["comments"]
        post.is_favorite = data["is_favorite"]
        return post

    def __str__(self):
        return f"Post #{self.id} by {self.author}: {self.content[:30]}"

    #Nodo simple

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    #Lista enlazada simple

class LinkedListSimple:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, data):
        new_node = Node(data)

        if not self.head:
            self.head = new_node
            self.tail = new_node

        else:
            self.tail.next = new_node
            self.tail = new_node

        self.size += 1

    def prepend(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

        if not self.tail:
            self.tail = new_node

        self.size += 1

    def count(self):
        return self.size

    def is_empty(self):
        return self.size == 0

    def get_all(self):
        result = []
        current = self.head

        while current:
            result.append(current.data)
            current = current.next

        return result

    def search(self, keyword):
        if not keyword:
            return []

        results = []
        current = self.head

        while current:
            if keyword.lower() in current.data.content.lower():
                results.append(current.data)

            current = current.next

        return results

    def get_by_index(self, index):

        if index < 0 or index >= self.size:
            return None

        current = self.head

        for _ in range(index):
            current = current.next

        return current.data

    def delete(self, data):
        if not self.head:
            return False

        if self.head.data == data:
            self.head = self.head.next
            if self.head is None:
                self.tail = None

            self.size -= 1
            return True

        current = self.head

        while current.next:
            if current.next.data == data:
                if current.next == self.tail:
                    self.tail = current

                current.next = current.next.next
                self.size -= 1
                return True
            current = current.next

        return False

    def get_tail(self):
        return self.tail.data if self.tail else None

    def find_by_id(self, post_id):
        current = self.head
        while current:
            if current.data.id == post_id:
                return current.data
            current = current.next
        return None

    def insert_at(self, index, data):
        if index < 0 or index > self.size:
            return False
        if index == 0:
            self.prepend(data)
            return True
        if index == self.size:
            self.append(data)
            return True
        new_node = Node(data)
        current = self.head
        for _ in range(index - 1):
            current = current.next
        new_node.next = current.next
        current.next = new_node

        self.size += 1
        return True

    #Nodo doble

class NodeDoubly:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

    #Lista Doblemente Enlazada

class LinkedListDoubly:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None
        self.size = 0

    def append(self, data):
        new_node = NodeDoubly(data)

        if not self.head:
            self.head = new_node
            self.tail = new_node
            self.current = new_node

        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

        self.size += 1

    def next_post(self):
        if not self.current:
            return None

        if self.current.next:
            self.current = self.current.next
            return self.current.data

        return None

    def prev_post(self):
        if not self.current:
            return None

        if self.current.prev:
            self.current = self.current.prev
            return self.current.data
        return None

    def get_current(self):
        if self.current:
            return self.current.data
        return None

    def reset_cursor(self):
        self.current = self.head

    def count(self):
        return self.size

    def find_by_id(self, post_id):
        current = self.head
        while current:
            if current.data.id == post_id:
                return current.data
            current = current.next
        return None

    def get_last(self):
        return self.tail.data if self.tail else None

    def get_all(self):
        result = []
        current = self.head

        while current:
            result.append(current.data)
            current = current.next

        return result

    #Lista Circular
class LinkedListCircular:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None
        self.size = 0

    def append(self, data):
        """Agrega un nodo al final de la lista."""
        new_node = Node(data)

        if not self.head:
            self.head = new_node
            self.tail = new_node
            new_node.next = self.head
            self.current = self.head

        else:
            self.tail.next = new_node
            self.tail = new_node
            new_node.next = self.head

        self.size += 1

    def next_post(self):
        if not self.current:
            return None

        self.current = self.current.next
        return self.current.data

    def get_current(self):
        if self.current:
            return self.current.data
        return None

    def reset_cursor(self):
        self.current = self.head

    def count(self):
        return self.size

    def exists_by_id(self, post_id):
        if not self.head:
            return False
        current = self.head

        while True:
            if current.data.id == post_id:
                return True
            current = current.next
            if current == self.head:
                break
        return False

    def get_all(self):
        result = []
        if not self.head:
            return result
        current = self.head

        while True:
            result.append(current.data)
            current = current.next
            if current == self.head:
                break

        return result