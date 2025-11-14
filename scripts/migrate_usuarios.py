#!/usr/bin/env python3
# Script para añadir columnas faltantes y normalizar roles en jubilados.db
import sqlite3

MAPPING_ROLES = {
    "Administrador": "admin",
    "admin": "admin",
    "Presidente": "presidente",
    "presidente": "presidente",
    "Secretario": "secretario",
    "secretario": "secretario",
    "Tesorero": "tesorero",
    "tesorero": "tesorero"
}

def column_exists(cursor, table, column):
    cursor.execute("PRAGMA table_info(%s)" % table)
    cols = [row[1] for row in cursor.fetchall()]
    return column in cols

def main():
    conn = sqlite3.connect("jubilados.db")
    cursor = conn.cursor()

    # Añadir columnas si no existen (SQLite permite ADD COLUMN)
    if not column_exists(cursor, "usuarios", "dni"):
        cursor.execute("ALTER TABLE usuarios ADD COLUMN dni TEXT")
        print("Añadida columna dni")
    if not column_exists(cursor, "usuarios", "contrasena"):
        cursor.execute("ALTER TABLE usuarios ADD COLUMN contrasena TEXT")
        print("Añadida columna contrasena")

    # Normalizar roles
    cursor.execute("SELECT id, rol FROM usuarios")
    rows = cursor.fetchall()
    for _id, rol in rows:
        if rol is None:
            continue
        nuevo = MAPPING_ROLES.get(rol.strip(), rol.strip().lower())
        if nuevo != rol:
            cursor.execute("UPDATE usuarios SET rol = ? WHERE id = ?", (nuevo, _id))
    conn.commit()

    # Mostrar conteo por rol
    cursor.execute("SELECT rol, COUNT(*) FROM usuarios GROUP BY rol")
    print("Conteo por rol:")
    for rol, cnt in cursor.fetchall():
        print(f"- {rol}: {cnt}")

    conn.close()

if __name__ == "__main__":
    main()