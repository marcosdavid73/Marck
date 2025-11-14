import tkinter as tk
from tkinter import messagebox
import sqlite3
from config import *
from menu import mostrar_dashboard

def verificar_login(usuario, contrasena, login_window):
    if not usuario or not contrasena:
        messagebox.showwarning("Campos vacíos", "Por favor completá ambos campos.")
        return

    conn = sqlite3.connect("jubilados.db")
    cursor = conn.cursor()
    cursor.execute("SELECT rol FROM usuarios WHERE nombre_usuario = ? AND contrasena = ?", (usuario, contrasena))
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        login_window.destroy()
        root = tk.Tk()
        root.withdraw()
        mostrar_dashboard(usuario, root)
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

def crear_entry_redondeado(parent, placeholder="", show=None):
    contenedor = tk.Frame(parent, bg="#ECEFF1")
    contenedor.pack(pady=10)

    canvas = tk.Canvas(contenedor, width=300, height=44, bg="#ECEFF1", highlightthickness=0)
    canvas.pack()
    canvas.create_oval(0, 0, 44, 44, fill="white", outline="white")
    canvas.create_oval(256, 0, 300, 44, fill="white", outline="white")
    canvas.create_rectangle(22, 0, 278, 44, fill="white", outline="white")

    entry = tk.Entry(contenedor, font=("Segoe UI Light", 12), bg="white", fg="#263238",
                     relief="flat", justify="center", show=show)
    entry.place(x=30, y=10, width=240, height=24)
    entry.insert(0, placeholder)
    entry.bind("<FocusIn>", lambda e: entry.delete(0, "end"))
    return entry

def mostrar_login():
    login_window = tk.Tk()
    login_window.iconbitmap("C:/Users/David/Daxdosoft/x.ico")
    login_window.title("Asociación Jubilados y Pensionados San Cayetano - Iniciar sesión")
    login_window.configure(bg="#ECEFF1")
    login_window.resizable(False, False)

    ancho_ventana = 1000
    alto_ventana = 600
    x = (login_window.winfo_screenwidth() - ancho_ventana) // 2
    y = (login_window.winfo_screenheight() - alto_ventana) // 2
    login_window.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

    tk.Label(login_window, text="Bienvenido", font=("Segoe UI Light", 28), bg="#ECEFF1", fg="#263238").pack(pady=(80, 10))
    tk.Label(login_window, text="Asociación Jubilados y Pensionados San Cayetano", font=("Segoe UI", 16), bg="#ECEFF1", fg="#455A64").pack(pady=(0, 30))

    entrada_usuario = crear_entry_redondeado(login_window, placeholder="Usuario")
    entrada_usuario.focus_set()

    entrada_contrasena = crear_entry_redondeado(login_window, placeholder="Contraseña", show="*")

    boton = tk.Button(
        login_window,
        text="Ingresar",
        font=("Segoe UI", 12),
        bg="#607D8B",
        fg="white",
        relief="flat",
        command=lambda: verificar_login(entrada_usuario.get(), entrada_contrasena.get(), login_window)
    )
    boton.pack(pady=30, ipadx=20, ipady=6)
    boton.bind("<Enter>", lambda e: boton.config(bg="#78909C"))
    boton.bind("<Leave>", lambda e: boton.config(bg="#607D8B"))

    login_window.bind("<Return>", lambda event: verificar_login(entrada_usuario.get(), entrada_contrasena.get(), login_window))

    login_window.mainloop()