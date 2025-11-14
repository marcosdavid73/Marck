import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from config import COLOR_FONDO

# --- Registrar movimiento en la base ---
def registrar_movimiento(fecha, tipo, concepto, monto, origen, usuario_id):
    conn = sqlite3.connect("jubilados.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO movimientos_caja (fecha, tipo, concepto, monto, origen, registrado_por)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (fecha, tipo, concepto, monto, origen, usuario_id))
    conn.commit()
    conn.close()

# --- Mostrar módulo de caja ---
def mostrar_caja(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Caja.TButton",
                    font=("Segoe UI", 11, "bold"),
                    foreground="white",
                    background="#3d5af1",
                    padding=10)
    style.map("Caja.TButton",
              background=[("active", "#455A64")])

    contenedor = tk.Frame(frame, bg=COLOR_FONDO)
    contenedor.pack(expand=True, fill="both")

    tk.Label(contenedor,
             text="💰 Movimientos de Caja",
             font=("Segoe UI", 20, "bold"),
             fg="#263238",
             bg=COLOR_FONDO).pack(pady=(20, 10))

    # --- Formulario de registro ---
    form = tk.Frame(contenedor, bg=COLOR_FONDO)
    form.pack(pady=10)

    campos = {}

    def campo(label_text):
        tk.Label(form, text=label_text, font=("Segoe UI", 11), bg=COLOR_FONDO).pack()
        entry = tk.Entry(form, font=("Segoe UI", 11), width=30, justify="center")
        entry.pack(pady=5)
        return entry

    campos["fecha"] = campo("Fecha (dd/mm/aaaa)")
    campos["tipo"] = ttk.Combobox(form, values=["ingreso", "egreso"], font=("Segoe UI", 11), state="readonly", width=28, justify="center")
    campos["tipo"].set("ingreso")
    campos["tipo"].pack(pady=5)

    campos["concepto"] = campo("Concepto")
    campos["monto"] = campo("Monto")
    campos["origen"] = campo("Origen (alquiler, evento, asistencia, otro)")

    def guardar():
        try:
            fecha = campos["fecha"].get()
            tipo = campos["tipo"].get()
            concepto = campos["concepto"].get()
            monto = float(campos["monto"].get())
            origen = campos["origen"].get()
            usuario_id = 1  # temporal

            registrar_movimiento(fecha, tipo, concepto, monto, origen, usuario_id)
            messagebox.showinfo("Registro exitoso", "Movimiento guardado correctamente.")
            for campo in campos.values():
                campo.delete(0, tk.END) if isinstance(campo, tk.Entry) else campo.set("ingreso")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {e}")

    ttk.Button(form, text="➕ Registrar movimiento", style="Caja.TButton", command=guardar).pack(pady=10)

    # --- Tabla de movimientos con scrollbar ---
    tabla_frame = tk.Frame(contenedor, bg=COLOR_FONDO)
    tabla_frame.pack(pady=10, fill="both", expand=True)

    scrollbar = ttk.Scrollbar(tabla_frame)
    scrollbar.pack(side="right", fill="y")

    tabla = ttk.Treeview(tabla_frame,
                         columns=("fecha", "tipo", "concepto", "monto", "origen"),
                         show="headings",
                         height=10,
                         yscrollcommand=scrollbar.set)
    scrollbar.config(command=tabla.yview)

    for col in ("fecha", "tipo", "concepto", "monto", "origen"):
        tabla.heading(col, text=col.capitalize())
        tabla.column(col, anchor="center", width=120)

    tabla.pack(fill="both", expand=True)

    # --- Cargar movimientos existentes ---
    conn = sqlite3.connect("jubilados.db")
    cursor = conn.cursor()
    cursor.execute("SELECT fecha, tipo, concepto, monto, origen FROM movimientos_caja ORDER BY fecha DESC")
    for fila in cursor.fetchall():
        tabla.insert("", "end", values=fila)
    conn.close()

    def campo(label_text):
        tk.Label(form, text=label_text, font=("Segoe UI", 11), bg=COLOR_FONDO).pack()
        entry = tk.Entry(form, font=("Segoe UI", 11), width=30)
        entry.pack(pady=5)
        return entry

    campos["fecha"] = campo("Fecha (dd/mm/aaaa)")
    campos["tipo"] = ttk.Combobox(form, values=["ingreso", "egreso"], font=("Segoe UI", 11), state="readonly", width=28)
    campos["tipo"].set("ingreso")
    campos["tipo"].pack(pady=5)

    campos["concepto"] = campo("Concepto")
    campos["monto"] = campo("Monto")
    campos["origen"] = campo("Origen (alquiler, evento, asistencia, otro)")

    def guardar():
        try:
            fecha = campos["fecha"].get()
            tipo = campos["tipo"].get()
            concepto = campos["concepto"].get()
            monto = float(campos["monto"].get())
            origen = campos["origen"].get()
            usuario_id = 1  # temporal, luego lo conectamos con el usuario activo

            registrar_movimiento(fecha, tipo, concepto, monto, origen, usuario_id)
            messagebox.showinfo("Registro exitoso", "Movimiento guardado correctamente.")
            for campo in campos.values():
                campo.delete(0, tk.END) if isinstance(campo, tk.Entry) else campo.set("ingreso")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {e}")

    ttk.Button(form, text="➕ Registrar movimiento", style="Caja.TButton", command=guardar).pack(pady=10)

    # --- Tabla de movimientos (placeholder) ---
    tabla = ttk.Treeview(contenedor, columns=("fecha", "tipo", "concepto", "monto", "origen"), show="headings")
    tabla.heading("fecha", text="Fecha")
    tabla.heading("tipo", text="Tipo")
    tabla.heading("concepto", text="Concepto")
    tabla.heading("monto", text="Monto")
    tabla.heading("origen", text="Origen")
    tabla.pack(pady=20, fill="both", expand=True)

    # --- Cargar movimientos existentes ---
    conn = sqlite3.connect("jubilados.db")
    cursor = conn.cursor()
    cursor.execute("SELECT fecha, tipo, concepto, monto, origen FROM movimientos_caja ORDER BY fecha DESC")
    for fila in cursor.fetchall():
        tabla.insert("", "end", values=fila)
    conn.close()