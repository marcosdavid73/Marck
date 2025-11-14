import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

ALQUILERES = []

def mostrar_alquileres(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    tk.Label(frame, text="Registro de Alquileres", font=("Segoe UI", 18, "bold"), fg="#263238", bg="#ECEFF1").pack(pady=(30, 10))

    estilo = ttk.Style()
    estilo.configure("Treeview",
                     font=("Segoe UI", 11),
                     rowheight=30,
                     background="white",
                     fieldbackground="white",
                     foreground="#263238")
    estilo.configure("Treeview.Heading",
                     font=("Segoe UI", 12, "bold"),
                     background="#607D8B",
                     foreground="black")

    tabla = ttk.Treeview(frame, columns=("tipo", "nombre", "fecha", "duracion"), show="headings", style="Treeview")
    tabla.heading("tipo", text="Espacio")
    tabla.heading("nombre", text="Nombre")
    tabla.heading("fecha", text="Fecha")
    tabla.heading("duracion", text="Duración")
    tabla.column("tipo", anchor="center", width=120)
    tabla.column("nombre", anchor="center", width=180)
    tabla.column("fecha", anchor="center", width=120)
    tabla.column("duracion", anchor="center", width=120)
    tabla.pack(padx=40, pady=10, fill="x")

    def cargar_alquileres():
        tabla.delete(*tabla.get_children())
        for a in ALQUILERES:
            tabla.insert("", "end", values=a)

    cargar_alquileres()

    def abrir_ventana_nuevo():
        ventana = tk.Toplevel(frame)
        ventana.title("Nuevo Alquiler")
        ventana.geometry("400x350")
        ventana.configure(bg="#ECEFF1")
        ventana.resizable(False, False)

        tk.Label(ventana, text="Registrar Alquiler", font=("Segoe UI", 16, "bold"), bg="#ECEFF1", fg="#263238").pack(pady=20)

        tipo = ttk.Combobox(ventana, font=("Segoe UI", 12), values=["Salón", "Box"])
        tipo.pack(pady=10, ipadx=10, ipady=4)
        tipo.set("Seleccionar espacio")

        nombre = tk.Entry(ventana, font=("Segoe UI", 12), justify="center")
        nombre.pack(pady=10, ipadx=40, ipady=6)
        nombre.insert(0, "Nombre del responsable")

        fecha = tk.Entry(ventana, font=("Segoe UI", 12), justify="center")
        fecha.pack(pady=10, ipadx=40, ipady=6)
        fecha.insert(0, date.today().strftime("%d/%m/%Y"))

        duracion = tk.Entry(ventana, font=("Segoe UI", 12), justify="center")
        duracion.pack(pady=10, ipadx=40, ipady=6)
        duracion.insert(0, "Ej: 1 día / 3 meses")

        def guardar():
            datos = (tipo.get(), nombre.get().strip(), fecha.get().strip(), duracion.get().strip())
            if "Seleccionar" in datos or "" in datos:
                messagebox.showwarning("Campos incompletos", "Por favor completá todos los campos.")
                return
            ALQUILERES.append(datos)
            cargar_alquileres()
            ventana.destroy()

        tk.Button(ventana, text="Guardar", font=("Segoe UI", 12), bg="#607D8B", fg="white", relief="flat", command=guardar).pack(pady=20, ipadx=20, ipady=6)

    tk.Button(frame, text="➕ Nuevo Alquiler", font=("Segoe UI", 12), bg="#3d5af1", fg="white", relief="flat", command=abrir_ventana_nuevo).pack(pady=20)