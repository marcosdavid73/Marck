import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Diccionario compartido de eventos por fecha (formato: "dd/mm/yyyy")
EVENTOS_REGISTRADOS = {}

def mostrar_eventos(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    tk.Label(frame, text="Registro de Eventos", font=("Segoe UI", 18, "bold"), fg="#263238", bg="#ECEFF1").pack(pady=(30, 10))

    tabla = ttk.Treeview(frame, columns=("fecha", "descripcion"), show="headings", style="Treeview")
    tabla.heading("fecha", text="Fecha")
    tabla.heading("descripcion", text="Descripción")
    tabla.column("fecha", anchor="center", width=120)
    tabla.column("descripcion", anchor="w", width=400)
    tabla.pack(padx=40, pady=10, fill="x")

    def cargar_eventos():
        tabla.delete(*tabla.get_children())
        for fecha, descripcion in EVENTOS_REGISTRADOS.items():
            tabla.insert("", "end", values=(fecha, descripcion))

    cargar_eventos()

    def abrir_ventana_nuevo():
        ventana = tk.Toplevel(frame)
        ventana.title("Nuevo Evento")
        ventana.geometry("400x300")
        ventana.configure(bg="#ECEFF1")
        ventana.resizable(False, False)

        tk.Label(ventana, text="Agregar Evento", font=("Segoe UI", 16, "bold"), bg="#ECEFF1", fg="#263238").pack(pady=20)

        entry_fecha = tk.Entry(ventana, font=("Segoe UI", 12), justify="center")
        entry_fecha.pack(pady=10, ipadx=40, ipady=6)
        entry_fecha.insert(0, datetime.today().strftime("%d/%m/%Y"))

        entry_desc = tk.Entry(ventana, font=("Segoe UI", 12), justify="center")
        entry_desc.pack(pady=10, ipadx=40, ipady=6)
        entry_desc.insert(0, "Descripción del evento")

        def guardar():
            fecha = entry_fecha.get().strip()
            descripcion = entry_desc.get().strip()
            try:
                datetime.strptime(fecha, "%d/%m/%Y")
            except ValueError:
                messagebox.showerror("Fecha inválida", "Usá el formato dd/mm/yyyy.")
                return
            if not descripcion:
                messagebox.showwarning("Campo vacío", "La descripción no puede estar vacía.")
                return
            EVENTOS_REGISTRADOS[fecha] = descripcion
            cargar_eventos()
            ventana.destroy()

        tk.Button(ventana, text="Guardar", font=("Segoe UI", 12), bg="#607D8B", fg="white", relief="flat", command=guardar).pack(pady=20, ipadx=20, ipady=6)

    tk.Button(frame, text="➕ Nuevo Evento", font=("Segoe UI", 12), bg="#3d5af1", fg="white", relief="flat", command=abrir_ventana_nuevo).pack(pady=20)