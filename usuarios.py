import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from config import COLOR_FONDO

def mostrar_usuarios(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Usuario.TButton",
                    font=("Segoe UI", 11, "bold"),
                    foreground="white",
                    background="#009688",
                    padding=10)
    style.map("Usuario.TButton",
              background=[("active", "#00796B")])

    tk.Label(frame, text="👥 Gestión de Usuarios", font=("Segoe UI", 20, "bold"), fg="#263238", bg=COLOR_FONDO).pack(pady=(30, 10))

    tabla = ttk.Treeview(frame, columns=("id", "usuario", "dni", "rol"), show="headings", style="Treeview", height=8)
    tabla.heading("id", text="ID")
    tabla.heading("usuario", text="Usuario")
    tabla.heading("dni", text="DNI")
    tabla.heading("rol", text="Rol")
    tabla.column("id", anchor="center", width=50)
    tabla.column("usuario", anchor="center", width=180)
    tabla.column("dni", anchor="center", width=120)
    tabla.column("rol", anchor="center", width=150)
    tabla.pack(padx=40, pady=10, fill="x")

    def cargar_usuarios():
        tabla.delete(*tabla.get_children())
        conn = sqlite3.connect("jubilados.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre_usuario, dni, rol FROM usuarios ORDER BY id ASC")
        for fila in cursor.fetchall():
            tabla.insert("", "end", values=fila)
        conn.close()

    cargar_usuarios()

    def abrir_ventana_agregar():
        ventana = tk.Toplevel(frame)
        ventana.title("Agregar Usuario")
        ventana.geometry("400x300")
        ventana.configure(bg=COLOR_FONDO)
        ventana.resizable(False, False)

        tk.Label(ventana, text="➕ Nuevo Usuario", font=("Segoe UI", 16, "bold"), bg=COLOR_FONDO, fg="#263238").pack(pady=20)

        entry_usuario = tk.Entry(ventana, font=("Segoe UI", 12), justify="center")
        entry_usuario.pack(pady=5, ipadx=40, ipady=6)
        entry_usuario.insert(0, "Nombre de usuario")

        entry_dni = tk.Entry(ventana, font=("Segoe UI", 12), justify="center")
        entry_dni.pack(pady=5, ipadx=40, ipady=6)
        entry_dni.insert(0, "DNI")

        entry_rol = ttk.Combobox(ventana, font=("Segoe UI", 12), values=["Administrador", "Presidente", "Secretario", "Tesorero"], state="readonly", justify="center")
        entry_rol.pack(pady=5, ipadx=10, ipady=4)
        entry_rol.set("Seleccionar rol")

        def guardar():
            usuario = entry_usuario.get().strip()
            dni = entry_dni.get().strip()
            rol = entry_rol.get().strip()
            if not usuario or not dni or rol == "Seleccionar rol":
                messagebox.showwarning("Campos incompletos", "Por favor completá todos los campos.")
                return
            try:
                conn = sqlite3.connect("jubilados.db")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO usuarios (nombre_usuario, dni, contrasena, rol) VALUES (?, ?, ?, ?)", (usuario, dni, "1234", rol))
                conn.commit()
                conn.close()
                messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
                cargar_usuarios()
                ventana.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Ese usuario o DNI ya existe.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar: {e}")

        tk.Button(ventana, text="Guardar", font=("Segoe UI", 12), bg="#607D8B", fg="white", relief="flat", command=guardar).pack(pady=20, ipadx=20, ipady=6)

    def eliminar_usuario():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Sin selección", "Seleccioná un usuario para eliminar.")
            return
        valores = tabla.item(seleccionado)["values"]
        usuario_id = valores[0]
        try:
            conn = sqlite3.connect("jubilados.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
            conn.commit()
            conn.close()
            cargar_usuarios()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar: {e}")

    def editar_usuario():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Sin selección", "Seleccioná un usuario para editar.")
            return
        valores = tabla.item(seleccionado)["values"]
        usuario_id, nombre_actual, dni_actual, rol_actual = valores

        ventana = tk.Toplevel(frame)
        ventana.title("Editar Usuario")
        ventana.geometry("400x300")
        ventana.configure(bg=COLOR_FONDO)
        ventana.resizable(False, False)

        tk.Label(ventana, text="✏️ Editar Usuario", font=("Segoe UI", 16, "bold"), bg=COLOR_FONDO, fg="#263238").pack(pady=20)

        entry_usuario = tk.Entry(ventana, font=("Segoe UI", 12), justify="center")
        entry_usuario.pack(pady=5, ipadx=40, ipady=6)
        entry_usuario.insert(0, nombre_actual)

        entry_dni = tk.Entry(ventana, font=("Segoe UI", 12), justify="center")
        entry_dni.pack(pady=5, ipadx=40, ipady=6)
        entry_dni.insert(0, dni_actual)

        entry_rol = ttk.Combobox(ventana, font=("Segoe UI", 12), values=["Administrador", "Presidente", "Secretario", "Tesorero"], state="readonly", justify="center")
        entry_rol.pack(pady=5, ipadx=10, ipady=4)
        entry_rol.set(rol_actual)

        def guardar_edicion():
            nuevo_usuario = entry_usuario.get().strip()
            nuevo_dni = entry_dni.get().strip()
            nuevo_rol = entry_rol.get().strip()
            if not nuevo_usuario or not nuevo_dni or nuevo_rol == "Seleccionar rol":
                messagebox.showwarning("Campos incompletos", "Por favor completá todos los campos.")
                return
            try:
                conn = sqlite3.connect("jubilados.db")
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE usuarios
                    SET nombre_usuario = ?, dni = ?, rol = ?
                    WHERE id = ?
                """, (nuevo_usuario, nuevo_dni, nuevo_rol, usuario_id))
                conn.commit()
                conn.close()
                cargar_usuarios()
                ventana.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Ese usuario o DNI ya existe.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo editar: {e}")

        tk.Button(ventana, text="Guardar Cambios", font=("Segoe UI", 12), bg="#607D8B", fg="white", relief="flat", command=guardar_edicion).pack(pady=20, ipadx=20, ipady=6)

    def cambiar_contrasena():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Sin selección", "Seleccioná un usuario para cambiar la contraseña.")
            return
        valores = tabla.item(seleccionado)["values"]
        usuario_id, nombre_usuario = valores[0], valores[1]

        ventana = tk.Toplevel(frame)
        ventana.title("Cambiar contraseña")
        ventana.geometry("400x250")
        ventana.configure(bg=COLOR_FONDO)
        ventana.resizable(False, False)

        tk.Label(ventana, text=f"🔐 Cambiar contraseña de {nombre_usuario}", font=("Segoe UI", 16, "bold"),
                 bg=COLOR_FONDO, fg="#263238").pack(pady=20)

        entry_nueva = tk.Entry(ventana, font=("Segoe UI", 12), justify="center", show="*")
        entry_nueva.pack(pady=10, ipadx=40, ipady=6)
        entry_nueva.focus_set()

        def guardar_nueva():
            nueva = entry_nueva.get().strip()
            if not nueva:
                messagebox.showwarning("Campo vacío", "Ingresá una nueva contraseña válida.")
                return
            try:
                conn = sqlite3.connect("jubilados.db")
                cursor = conn.cursor()
                cursor.execute("UPDATE usuarios SET contrasena = ? WHERE id = ?", (nueva, usuario_id))
                conn.commit()
                conn.close()
                messagebox.showinfo("Éxito", "Contraseña actualizada correctamente.")
                ventana.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar: {e}")

        tk.Button(ventana, text="Guardar", font=("Segoe UI", 12), bg="#607D8B", fg="white",
                  relief="flat", command=guardar_nueva).pack(pady=20, ipadx=20, ipady=6)

    # Botones principales
    botones_frame = tk.Frame(frame, bg=COLOR_FONDO)
    botones_frame.pack(pady=20)

    tk.Button(botones_frame, text="➕ Agregar", font=("Segoe UI", 12), bg="#3d5af1", fg="white",
              relief="flat", command=abrir_ventana_agregar).pack(side="left", padx=10, ipadx=10, ipady=6)

    tk.Button(botones_frame, text="✏️ Editar", font=("Segoe UI", 12), bg="#FFB300", fg="white",
              relief="flat", command=editar_usuario).pack(side="left", padx=10, ipadx=10, ipady=6)

    tk.Button(botones_frame, text="🗑️ Eliminar", font=("Segoe UI", 12), bg="#E53935", fg="white",
              relief="flat", command=eliminar_usuario).pack(side="left", padx=10, ipadx=10, ipady=6)

    tk.Button(botones_frame, text="🔐 Cambiar contraseña", font=("Segoe UI", 12), bg="#5C6BC0", fg="white",
              relief="flat", command=cambiar_contrasena).pack(side="left", padx=10, ipadx=10, ipady=6)