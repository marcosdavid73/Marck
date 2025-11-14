import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from config import COLOR_FONDO, FUENTE_TITULO, MODULOS_POR_ROL
from usuarios import mostrar_usuarios
from afiliados import mostrar_afiliados
from eventos import mostrar_eventos, EVENTOS_REGISTRADOS
from alquileres import mostrar_alquileres
from caja import mostrar_caja
import sqlite3

# --- Vista principal: Acciones rápidas ---
def mostrar_inicio(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    style = ttk.Style()
    style.theme_use("clam")

    colores = {
        "Asistencia.TButton": "#3d5af1",
        "Evento.TButton": "#009688",
        "Signos.TButton": "#e91e63",
        "Economica.TButton": "#ff9800"
    }

    for nombre_estilo, color in colores.items():
        style.configure(nombre_estilo,
                        font=("Segoe UI", 12, "bold"),
                        foreground="white",
                        background=color,
                        padding=10)
        style.map(nombre_estilo,
                  background=[("active", "#455A64")])

    contenedor = tk.Frame(frame, bg=COLOR_FONDO)
    contenedor.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(contenedor,
             text="⚡ Acciones rápidas",
             font=("Segoe UI", 20, "bold"),
             fg="#263238",
             bg=COLOR_FONDO).pack(pady=(0, 30))

    grid_frame = tk.Frame(contenedor, bg=COLOR_FONDO)
    grid_frame.pack()

    acciones = [
        ("🧺 Agregar asistencia social", mostrar_asistencias, "Asistencia.TButton"),
        ("📅 Agregar evento", mostrar_eventos, "Evento.TButton"),
        ("❤️ Registrar signos vitales", mostrar_signos_vitales, "Signos.TButton"),
        ("💸 Registrar ayuda económica", mostrar_ayuda_economica, "Economica.TButton")
    ]

    for i, (texto, funcion, estilo) in enumerate(acciones):
        b = ttk.Button(grid_frame,
                       text=texto,
                       style=estilo,
                       command=lambda f=funcion: f(frame))
        b.grid(row=i // 2, column=i % 2, padx=20, pady=20, ipadx=20, ipady=20)

# --- Obtener rol desde la base de datos ---
def obtener_rol(usuario):
    conn = sqlite3.connect("jubilados.db")
    cursor = conn.cursor()
    cursor.execute("SELECT rol FROM usuarios WHERE nombre_usuario = ?", (usuario,))
    resultado = cursor.fetchone()
    conn.close()
    if resultado:
        ROL_MAPEADO = {
            "administrador": "admin",
            "presidente": "presidente",
            "secretario": "secretario",
            "tesorero": "tesorero"
        }
        return ROL_MAPEADO.get(resultado[0].lower(), "tesorero")
    return "tesorero"

# --- Panel de afiliados con submódulos ---
def mostrar_panel_afiliados(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Submenu.TButton",
                    font=("Segoe UI", 12, "bold"),
                    foreground="white",
                    background="#607D8B",
                    padding=10)
    style.map("Submenu.TButton",
              background=[("active", "#455A64")])

    contenedor = tk.Frame(frame, bg=COLOR_FONDO)
    contenedor.pack(expand=True)

    tk.Label(contenedor,
             text="👥 Panel de Afiliados",
             font=("Segoe UI", 20, "bold"),
             fg="#263238",
             bg=COLOR_FONDO).pack(pady=(20, 10))

    botones = [
        ("📋 Lista de afiliados", mostrar_afiliados),
        ("🧺 Asistencias sociales", mostrar_asistencias),
        ("📦 Entregas realizadas", mostrar_entregas),
        ("❤️ Historial de signos vitales", mostrar_signos_vitales)
    ]

    for texto, funcion in botones:
        b = ttk.Button(contenedor,
                       text=texto,
                       style="Submenu.TButton",
                       command=lambda f=funcion: f(frame))
        b.pack(pady=10, ipadx=20, ipady=10, fill="x", padx=60)

# --- Submódulos vacíos ---
def mostrar_asistencias(frame):
    for widget in frame.winfo_children():
        widget.destroy()
    tk.Label(frame, text="🧺 Asistencias sociales", font=("Segoe UI", 18), bg=COLOR_FONDO).pack(pady=20)

def mostrar_entregas(frame):
    for widget in frame.winfo_children():
        widget.destroy()
    tk.Label(frame, text="📦 Entregas realizadas", font=("Segoe UI", 18), bg=COLOR_FONDO).pack(pady=20)

def mostrar_signos_vitales(frame):
    for widget in frame.winfo_children():
        widget.destroy()
    tk.Label(frame, text="❤️ Historial de signos vitales", font=("Segoe UI", 18), bg=COLOR_FONDO).pack(pady=20)

def mostrar_ayuda_economica(frame):
    for widget in frame.winfo_children():
        widget.destroy()
    tk.Label(frame, text="💸 Registrar ayuda económica", font=("Segoe UI", 18), bg=COLOR_FONDO).pack(pady=20)

# --- Dashboard principal ---
def mostrar_dashboard(usuario, root):
    rol = obtener_rol(usuario)

    root.title("Asociación de Jubilados y Pensionados")
    root.configure(bg=COLOR_FONDO)
    root.iconbitmap("C:/Users/David/Daxdosoft/x.ico")

    ancho_ventana = 1000
    alto_ventana = 600
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (ancho_ventana // 2)
    y = (root.winfo_screenheight() // 2) - (alto_ventana // 2)
    root.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

    frame_menu = tk.Frame(root, bg="#263238", width=180)
    frame_menu.pack(side="left", fill="y")

    frame_contenido = tk.Frame(root, bg=COLOR_FONDO)
    frame_contenido.pack(side="right", expand=True, fill="both")

    boton_activo = {"ref": None}

    def actualizar_estilo_activo(boton):
        if boton_activo["ref"]:
            boton_activo["ref"].configure(bg="#263238")
        if boton:
            boton.configure(bg="#455A64")
            boton_activo["ref"] = boton

    def cargar_modulo(funcion, boton):
        actualizar_estilo_activo(boton)
        for widget in frame_contenido.winfo_children():
            widget.destroy()
        try:
            funcion(frame_contenido)
        except Exception as e:
            print(f"Error al cargar módulo: {e}")

    def cerrar_sistema():
        root.destroy()
        from login import mostrar_login
        mostrar_login()

    acciones = []
    if "inicio" in MODULOS_POR_ROL[rol]:
        acciones.append(("🏠 Inicio", mostrar_inicio))
    if "usuarios" in MODULOS_POR_ROL[rol]:
        acciones.append(("👥 Usuarios", mostrar_usuarios))
    if "afiliados" in MODULOS_POR_ROL[rol]:
        acciones.append(("👥 Afiliados", mostrar_panel_afiliados))
    if "caja" in MODULOS_POR_ROL[rol]:
        acciones.append(("💰 Caja", mostrar_caja))
    if "eventos" in MODULOS_POR_ROL[rol]:
        acciones.append(("📅 Eventos", mostrar_eventos))
    if "alquileres" in MODULOS_POR_ROL[rol]:
        acciones.append(("📋 Alquileres", mostrar_alquileres))

    acciones.append(("🚪 Salir", lambda: cerrar_sistema()))

    tk.Label(frame_menu, text=f"{usuario.capitalize()}", bg="#263238", fg="white", font=FUENTE_TITULO).pack(pady=20)

    for texto, funcion in acciones:
        b = tk.Button(
            frame_menu,
            text=texto,
            bg="#263238",
            fg="white",
            font=("Segoe UI", 12),
            relief="flat",
            activebackground="#86C0DD",
            anchor="w",
            padx=20
        )
        b.configure(command=lambda f=funcion, btn=b: cargar_modulo(f, btn))
        b.pack(fill="x", pady=5)

    cargar_modulo(mostrar_inicio, None)
    root.deiconify()
    root.mainloop()