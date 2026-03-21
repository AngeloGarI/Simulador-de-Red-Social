import sqlite3

conn = sqlite3.connect("fakebook.db")
cursor = conn.cursor()

def inicializar():

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT UNIQUE,
    password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS publicaciones(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT,
    contenido TEXT,
    fecha TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS likes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT,
    post_id INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dislikes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT,
    post_id INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS amigos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario1 TEXT,
    usuario2 TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mensajes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    emisor TEXT,
    receptor TEXT,
    mensaje TEXT,
    fecha TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notificaciones(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT,
    texto TEXT,
    referencia TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notificaciones(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT,
    mensaje TEXT
    )
    """)

    conn.commit()

    print("Base de datos lista.")