from tkinter import ttk

def configurar_estilo_tablas():
    estilo = ttk.Style()
    estilo.configure("Treeview",
                     font=("Segoe UI", 11),
                     rowheight=30,
                     background="white",
                     fieldbackground="white",
                     foreground="#263238")
    estilo.configure("Treeview.Heading",
                     font=("Segoe UI", 12, "bold"),
                     relief="flat")
    estilo.map("Treeview.Heading",
               background=[("active", "#78909C"), ("!active", "#455A64")],
               foreground=[("!disabled", "black")])

MODULOS_POR_ROL = {
    "admin": ["inicio", "usuarios", "afiliados", "caja", "eventos", "alquileres"],
    "presidente": ["inicio", "afiliados", "caja", "eventos", "alquileres"],
    "secretario": ["inicio", "afiliados", "eventos", "alquileres"],
    "tesorero": ["inicio", "caja", "eventos"]
}

COLOR_FONDO = "#e3f2fd"
COLOR_BOTON = "#2196f3"
COLOR_BOTON_HOVER = "#1976d2"
COLOR_ENTRADA = "#bbdefb"
COLOR_TEXTO = "#0d47a1"
FUENTE = ("Segoe UI", 12)
FUENTE_TITULO = ("Segoe UI", 18)
ICONO_VENTANA = "x.ico"