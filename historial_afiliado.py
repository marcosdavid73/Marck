import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime
from config import COLOR_FONDO

def fecha_actual():
    return datetime.now().strftime("%Y-%m-%d")

def mostrar_historial_afiliado(afiliado_id):
    ventana = tk.Toplevel()
    ventana.title("Historial del Afiliado")
    ventana.geometry("800x500")
    ventana.configure(bg=COLOR_FONDO)
    ventana.resizable(False, False)

    notebook = ttk.Notebook(ventana)
    notebook.pack(expand=True, fill="both", padx=10, pady=10)

    # --- Datos personales ---
    tab_datos = tk.Frame(notebook, bg=COLOR_FONDO)
    notebook.add(tab_datos, text="📋 Datos personales")

    conn = sqlite3.connect("jubilados.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, dni, fecha_nacimiento, localidad FROM afiliados WHERE id = ?", (afiliado_id,))
    datos = cursor.fetchone()
    conn.close()

    if datos:
        nombre, dni, nacimiento, localidad = datos
        tk.Label(tab_datos, text=f"👤 Nombre: {nombre}", font=("Segoe UI", 12), bg=COLOR_FONDO).pack(pady=10)
        tk.Label(tab_datos, text=f"🆔 DNI: {dni}", font=("Segoe UI", 12), bg=COLOR_FONDO).pack(pady=10)
        tk.Label(tab_datos, text=f"🎂 Nacimiento: {nacimiento}", font=("Segoe UI", 12), bg=COLOR_FONDO).pack(pady=10)
        tk.Label(tab_datos, text=f"📍 Localidad: {localidad}", font=("Segoe UI", 12), bg=COLOR_FONDO).pack(pady=10)

    # --- Asistencias sociales ---
    tab_asistencias = tk.Frame(notebook, bg=COLOR_FONDO)
    notebook.add(tab_asistencias, text="🧺 Asistencias")

    tabla_asistencias = ttk.Treeview(tab_asistencias, columns=("fecha", "tipo"), show="headings", height=10)
    tabla_asistencias.heading("fecha", text="Fecha")
    tabla_asistencias.heading("tipo", text="Tipo")
    tabla_asistencias.pack(padx=20, pady=20, fill="x")

    conn = sqlite3.connect("jubilados.db")
    cursor = conn.cursor()
    cursor.execute("SELECT fecha, tipo FROM asistencias WHERE afiliado_id = ? ORDER BY fecha DESC", (afiliado_id,))
    for fila in cursor.fetchall():
        tabla_asistencias.insert("", "end", values=fila)
    conn.close()

    def registrar_asistencia():
        ventana = tk.Toplevel()
        ventana.title("Registrar asistencia")
        ventana.geometry("300x200")
        ventana.configure(bg=COLOR_FONDO)
        ventana.resizable(False, False)

        tipo_var = tk.StringVar()
        tipo_menu = ttk.Combobox(ventana, textvariable=tipo_var, values=["almuerzo", "vianda"], state="readonly", font=("Segoe UI", 12))
        tipo_menu.pack(pady=20)
        tipo_menu.set("Seleccionar tipo")

        def guardar():
            tipo = tipo_var.get()
            if tipo == "Seleccionar tipo":
                return
            conn = sqlite3.connect("jubilados.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO asistencias (afiliado_id, fecha, tipo) VALUES (?, ?, ?)", (afiliado_id, fecha_actual(), tipo))
            conn.commit()
            conn.close()
            tabla_asistencias.insert("", 0, values=(fecha_actual(), tipo))
            ventana.destroy()

        tk.Button(ventana, text="Guardar", font=("Segoe UI", 12), bg="#4CAF50", fg="white", command=guardar).pack(pady=10)

    tk.Button(tab_asistencias, text="➕ Registrar asistencia", font=("Segoe UI", 11), bg="#009688", fg="white", command=registrar_asistencia).pack(pady=10)

    # --- Signos vitales ---
    tab_signos = tk.Frame(notebook, bg=COLOR_FONDO)
    notebook.add(tab_signos, text="❤️ Signos vitales")

    tabla_signos = ttk.Treeview(tab_signos, columns=("fecha", "presion", "glucosa", "temperatura"), show="headings", height=10)
    for col in tabla_signos["columns"]:
        tabla_signos.heading(col, text=col.capitalize())
    tabla_signos.pack(padx=20, pady=20, fill="x")

    conn = sqlite3.connect("jubilados.db")
    cursor = conn.cursor()
    cursor.execute("SELECT fecha, presion, glucosa, temperatura FROM signos_vitales WHERE afiliado_id = ? ORDER BY fecha DESC", (afiliado_id,))
    for fila in cursor.fetchall():
        tabla_signos.insert("", "end", values=fila)
    conn.close()

    def registrar_signos():
        ventana = tk.Toplevel()
        ventana.title("Registrar signos vitales")
        ventana.geometry("350x300")
        ventana.configure(bg=COLOR_FONDO)
        ventana.resizable(False, False)

        campos = {}
        for campo in ["Presión", "Glucosa", "Temperatura"]:
            tk.Label(ventana, text=campo, bg=COLOR_FONDO).pack()
            entrada = tk.Entry(ventana, font=("Segoe UI", 12))
            entrada.pack(pady=5)
            campos[campo.lower()] = entrada

        def guardar():
            presion = campos["presión"].get().strip()
            glucosa = campos["glucosa"].get().strip()
            temperatura = campos["temperatura"].get().strip()
            conn = sqlite3.connect("jubilados.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO signos_vitales (afiliado_id, fecha, presion, glucosa, temperatura) VALUES (?, ?, ?, ?, ?)",
                           (afiliado_id, fecha_actual(), presion, glucosa, temperatura))
            conn.commit()
            conn.close()
            tabla_signos.insert("", 0, values=(fecha_actual(), presion, glucosa, temperatura))
            ventana.destroy()

        tk.Button(ventana, text="Guardar", font=("Segoe UI", 12), bg="#4CAF50", fg="white", command=guardar).pack(pady=10)

    tk.Button(tab_signos, text="➕ Registrar signos", font=("Segoe UI", 11), bg="#E91E63", fg="white", command=registrar_signos).pack(pady=10)

    # --- Entregas económicas ---
    tab_entregas = tk.Frame(notebook, bg=COLOR_FONDO)
    notebook.add(tab_entregas, text="💸 Entregas económicas")

    tabla_entregas = ttk.Treeview(tab_entregas, columns=("fecha", "tipo", "monto"), show="headings", height=10)
    for col in tabla_entregas["columns"]:
        tabla_entregas.heading(col, text=col.capitalize())
    tabla_entregas.pack(padx=20, pady=20, fill="x")

    conn = sqlite3.connect("jubilados.db")
    cursor = conn.cursor()
    cursor.execute("SELECT fecha, tipo, monto FROM entregas_economicas WHERE afiliado_id = ? ORDER BY fecha DESC", (afiliado_id,))
    for fila in cursor.fetchall():
        tabla_entregas.insert("", "end", values=fila)
    conn.close()

    def registrar_entrega():
        ventana = tk.Toplevel()
        ventana.title("Registrar entrega económica")
        ventana.geometry("350x250")
        ventana.configure(bg=COLOR_FONDO)
        ventana.resizable(False, False)

        tipo = tk.Entry(ventana, font=("Segoe UI", 12))
        tipo.pack(pady=10)
        tipo.insert(0, "Tipo de ayuda")

        monto = tk.Entry(ventana, font=("Segoe UI", 12))
        monto.pack(pady=10)
        monto.insert(0, "Monto")

        def guardar():
            tipo_val = tipo.get().strip()
            monto_val = monto.get().strip()
            conn = sqlite3.connect("jubilados.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO entregas_economicas (afiliado_id, fecha, tipo, monto) VALUES (?, ?, ?, ?)",
                           (afiliado_id, fecha_actual(), tipo_val, monto_val))
            conn.commit()
            conn.close()
            tabla_entregas.insert("", 0, values=(fecha_actual(), tipo_val, monto_val))
            ventana.destroy()

        tk.Button(ventana, text="Guardar", font=("Segoe UI", 12), bg="#4CAF50", fg="white", command=guardar).pack(pady=10)

    tk.Button(tab_entregas, text="➕ Registrar entrega", font=("Segoe UI", 11), bg="#FF9800", fg="white", command=registrar_entrega).pack(pady=10)