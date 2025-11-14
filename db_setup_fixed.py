# Versión sugerida de db_setup: crea la tabla usuarios con dni y contrasena
import sqlite3

def crear_base_datos():
    conn = sqlite3.connect("jubilados.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_usuario TEXT UNIQUE NOT NULL,
        dni TEXT UNIQUE,
        contrasena TEXT,
        rol TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS afiliados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        dni TEXT UNIQUE NOT NULL,
        telefono TEXT,
        direccion TEXT,
        nacimiento TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS eventos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        creado_por INTEGER,
        FOREIGN KEY (creado_por) REFERENCES usuarios(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alquileres (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        espacio TEXT NOT NULL,
        nombre_cliente TEXT NOT NULL,
        contacto TEXT,
        monto REAL NOT NULL,
        observaciones TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movimientos_caja (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        tipo TEXT CHECK(tipo IN ('ingreso', 'egreso')) NOT NULL,
        concepto TEXT NOT NULL,
        monto REAL NOT NULL,
        origen TEXT,
        alquiler_id INTEGER,
        registrado_por INTEGER,
        FOREIGN KEY (alquiler_id) REFERENCES alquileres(id),
        FOREIGN KEY (registrado_por) REFERENCES usuarios(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS asistencias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        tipo TEXT NOT NULL,
        detalle TEXT,
        afiliado_id INTEGER NOT NULL,
        monto REAL,
        entregado_por INTEGER,
        FOREIGN KEY (afiliado_id) REFERENCES afiliados(id),
        FOREIGN KEY (entregado_por) REFERENCES usuarios(id)
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Base de datos creada correctamente.")

if __name__ == "__main__":
    crear_base_datos()