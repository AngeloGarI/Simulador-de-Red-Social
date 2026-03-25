from estructuras import Post, LinkedListSimple, LinkedListDoubly, LinkedListCircular

def test_post():
    post = Post("Angelo", "Hola mundo")

    print("ID:", post.id)
    print("Autor:", post.author)
    print("Contenido:", post.content)
    print("Timestamp:", post.timestamp)

    data = post.to_dict()
    print("Convertido a dict:", data)

    nuevo = Post.from_dict(data)
    print("Reconstruido:", nuevo)

def test_lista_simple():

    lista = LinkedListSimple()

    p1 = Post("Ana", "Primer post")
    p2 = Post("Luis", "Segundo post")
    p3 = Post("Mario", "Tercer post")

    lista.append(p1)
    lista.append(p2)
    lista.prepend(p3)

    print("Cantidad:", lista.count())

    print("Todos los posts:")
    for post in lista.get_all():
        print(post)

    print("Buscar 'Segundo':")
    resultados = lista.search("Segundo")
    for r in resultados:
        print(r)

    print("Eliminar p2")
    lista.delete(p2)

    print("Cantidad después de eliminar:", lista.count())

def test_lista_doble():

    lista = LinkedListDoubly()

    p1 = Post("Ana", "Post A")
    p2 = Post("Luis", "Post B")
    p3 = Post("Mario", "Post C")

    lista.append(p1)
    lista.append(p2)
    lista.append(p3)

    print("Actual:", lista.get_current())

    print("Siguiente:", lista.next_post())
    print("Siguiente:", lista.next_post())

    print("Anterior:", lista.prev_post())

def test_lista_circular():

    lista = LinkedListCircular()

    p1 = Post("Ana", "Post 1")
    p2 = Post("Luis", "Post 2")
    p3 = Post("Mario", "Post 3")

    lista.append(p1)
    lista.append(p2)
    lista.append(p3)

    print("Actual:", lista.get_current())

    for _ in range(5):
        print("Siguiente:", lista.next_post())

if __name__ == "__main__":
    print("===== TEST POST =====")
    test_post()

    print("\n===== TEST LISTA SIMPLE =====")
    test_lista_simple()

    print("\n===== TEST LISTA DOBLE =====")
    test_lista_doble()

    print("\n===== TEST LISTA CIRCULAR =====")
    test_lista_circular()