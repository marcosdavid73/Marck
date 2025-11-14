import tkinter as tk
from tkinter import ttk, messagebox
from config import configurar_estilo_tablas, COLOR_FONDO
from historial_afiliado import mostrar_historial_afiliado  # Asegurate de tener este archivo

afiliados = [
    {"id": 1, "nombre": "Carlos Pérez", "dni": "12345678", "telefono": "3874123456", "direccion": "Calle Falsa 123", "nacimiento": "01/01/1950"},
    {"id": 2, "nombre": "Ana Gómez", "dni": "87654321", "telefono": "3874987654", "direccion": "Av. Libertad 456", "nacimiento": "15/03/1955"},
    {"id": 3, "nombre": "Luis Martínez", "dni": "11223344", "telefono": "3874001122", "direccion": "San Martín 789", "nacimiento": "22/07/1948"}
]

def mostrar_afiliados(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    configurar_estilo_tablas()

    tk.Label(frame, text="Gestión de Afiliados", font=("Segoe UI", 18, "bold"), fg="#263238", bg=COLOR_FONDO).pack(pady=(30, 10))

    filtro_var = tk.StringVar()
    entry_busqueda = tk.Entry(frame, textvariable=filtro_var, font=("Segoe UI", 12), justify="center")
    entry_busqueda.pack(pady=10, ipadx=80, ipady=6)
    entry_busqueda.insert(0, "Buscar por nombre o DNI")

    columnas = ("id", "nombre", "dni", "telefono", "direccion", "nacimiento")
    tabla = ttk.Treeview(frame, columns=columnas, show="headings", style="Treeview")
    for col in columnas:
        tabla.heading(col, text=col.capitalize())
        tabla.column(col, anchor="center", width=120)
    tabla.pack(padx=40, pady=10, fill="x")

    def cargar_afiliados(filtro=""):
        tabla.delete(*tabla.get_children())
        for a in afiliados:
            if filtro.lower() in a["nombre"].lower() or filtro in a["dni"]:
                tabla.insert("", "end", values=(a["id"], a["nombre"], a["dni"], a["telefono"], a["direccion"], a["nacimiento"]))

    cargar_afiliados()

    def actualizar_busqueda(*args):
        cargar_afiliados(filtro_var.get())

    filtro_var.trace_add("write", actualizar_busqueda)

    def abrir_ventana_nuevo():
        ventana = tk.Toplevel(frame)
        ventana.title("Nuevo Afiliado")
        ventana.geometry("400x450")
        ventana.configure(bg=COLOR_FONDO)
        ventana.resizable(False, False)

        tk.Label(ventana, text="Agregar Nuevo Afiliado", font=("Segoe UI", 16, "bold"), bg=COLOR_FONDO, fg="#263238").pack(pady=20)

        campos = {}
        for etiqueta in ["Nombre completo", "DNI", "Teléfono", "Dirección", "Fecha de nacimiento"]:
            tk.Label(ventana, text=etiqueta + ":", bg=COLOR_FONDO, anchor="w").pack(fill="x", padx=30)
            entrada = tk.Entry(ventana, font=("Segoe UI", 12))
            entrada.pack(fill="x", padx=30, pady=5)
            campos[etiqueta.lower()] = entrada

        def guardar():
            datos = {k: v.get().strip() for k, v in campos.items()}
            if "" in datos.values():
                messagebox.showwarning("Campos incompletos", "Por favor completá todos los campos.")
                return
            nuevo_id = max([a["id"] for a in afiliados]) + 1 if afiliados else 1
            afiliados.append({
                "id": nuevo_id,
                "nombre": datos["nombre completo"],
                "dni": datos["dni"],
                "telefono": datos["teléfono"],
                "direccion": datos["dirección"],
                "nacimiento": datos["fecha de nacimiento"]
            })
            cargar_afiliados()
            ventana.destroy()

        tk.Button(ventana, text="Guardar", font=("Segoe UI", 12), bg="#4CAF50", fg="white", relief="flat", command=guardar).pack(pady=20, ipadx=20, ipady=6)

    def eliminar_afiliado():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Sin selección", "Seleccioná un afiliado para eliminar.")
            return
        valores = tabla.item(seleccionado)["values"]
        afiliado_id = valores[0]
        confirmacion = messagebox.askyesno("Confirmar", "¿Estás seguro de que querés eliminar este afiliado?")
        if confirmacion:
            global afiliados
            afiliados = [a for a in afiliados if a["id"] != afiliado_id]
            cargar_afiliados()

    def abrir_historial():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Sin selección", "Seleccioná un afiliado para ver su historial.")
            return
        valores = tabla.item(seleccionado)["values"]
        afiliado_id = valores[0]
        mostrar_historial_afiliado(afiliado_id)

    botones_frame = tk.Frame(frame, bg=COLOR_FONDO)
    botones_frame.pack(pady=20)

    tk.Button(botones_frame, text="➕ Nuevo", font=("Segoe UI", 12), bg="#3d5af1", fg="white",
              relief="flat", command=abrir_ventana_nuevo).pack(side="left", padx=10, ipadx=10, ipady=6)

    tk.Button(botones_frame, text="🗑️ Eliminar", font=("Segoe UI", 12), bg="#E53935", fg="white",
              relief="flat", command=eliminar_afiliado).pack(side="left", padx=10, ipadx=10, ipady=6)

    tk.Button(botones_frame, text="📋 Ver historial", font=("Segoe UI", 12), bg="#5C6BC0", fg="white",
              relief="flat", command=abrir_historial).pack(side="left", padx=10, ipadx=10, ipady=6)