import tkinter as tk
from tkinter import messagebox
from config import *

datos_ingresos = [
    ("01/08/2025", "$50.000", "Municipalidad", "Mensual", "Subsidio operativo"),
    ("15/07/2025", "$30.000", "Ministerio", "Extraordinario", "Reparación techos"),
]

def registrar_ingreso(frame_padre):
    frame = tk.Frame(frame_padre, bg="#ECEFF1")
    frame.pack(fill="both", expand=True)

    # Título
    tk.Label(frame, text="Registrar Ingreso", font=("Segoe UI", 16, "bold"), bg="#ECEFF1").pack(pady=10)

    # Formulario
    form_frame = tk.Frame(frame, bg="#ECEFF1")
    form_frame.pack(pady=5)

    campos = {}
    etiquetas = [
        "Fecha (dd/mm/aaaa)",
        "Monto recibido",
        "Fuente",
        "Tipo de financiación",
        "Observaciones"
    ]

    for i, texto in enumerate(etiquetas):
        fila = tk.Frame(form_frame, bg="#ECEFF1")
        fila.pack(fill="x", padx=20, pady=3)
        tk.Label(fila, text=texto, bg="#ECEFF1", font=("Segoe UI", 11), width=20, anchor="w").pack(side="left")
        entrada = tk.Entry(fila, font=("Segoe UI", 11), width=30)
        entrada.pack(side="left", padx=5)
        campos[texto] = entrada

    mensaje_error = tk.Label(frame, text="", fg="red", bg="#ECEFF1", font=("Segoe UI", 10))
    mensaje_error.pack(pady=5)

    def guardar():
        datos = {k: v.get().strip() for k, v in campos.items()}
        if not all(datos.values()):
            mensaje_error.config(text="Por favor completá todos los campos.")
            return
        datos_ingresos.append(tuple(datos.values()))
        messagebox.showinfo("Registro exitoso", "Ingreso registrado correctamente.")
        for entrada in campos.values():
            entrada.delete(0, tk.END)
        mensaje_error.config(text="")
        actualizar_tabla()

    tk.Button(frame, text="Guardar", command=guardar, bg="#4CAF50", fg="white", font=("Segoe UI", 11), relief="flat").pack(pady=10)

    # Historial con scroll
    tk.Label(frame, text="Historial de Ingresos", font=("Segoe UI", 14, "bold"), bg="#ECEFF1").pack(pady=10)

    contenedor_tabla = tk.Frame(frame, bg="#ECEFF1")
    contenedor_tabla.pack(fill="both", expand=True, padx=10, pady=5)

    canvas = tk.Canvas(contenedor_tabla, bg="#ECEFF1", highlightthickness=0)
    scrollbar = tk.Scrollbar(contenedor_tabla, orient="vertical", command=canvas.yview)
    tabla_frame = tk.Frame(canvas, bg="#ECEFF1")

    tabla_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=tabla_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def actualizar_tabla():
        for widget in tabla_frame.winfo_children():
            widget.destroy()

        columnas = ["Fecha", "Monto", "Fuente", "Tipo", "Observaciones"]
        for i, col in enumerate(columnas):
            tk.Label(tabla_frame, text=col, font=("Segoe UI", 11, "bold"), bg="#B0BEC5", fg="black", width=15).grid(row=0, column=i, padx=2, pady=2)

        for fila, ingreso in enumerate(datos_ingresos, start=1):
            for col, valor in enumerate(ingreso):
                tk.Label(tabla_frame, text=valor, font=("Segoe UI", 11), bg="#ECEFF1", fg="black", width=15).grid(row=fila, column=col, padx=2, pady=2)

    actualizar_tabla()