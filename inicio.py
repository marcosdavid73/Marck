from tkinter import ttk
from tkcalendar import Calendar
import tkinter as tk
from config import *

def mostrar_inicio(parent):
    tk.Label(parent, text="Inicio", font=FUENTE_TITULO, bg=COLOR_FONDO).pack(pady=10)

    calendario = Calendar(parent, selectmode="day", date_pattern="dd/mm/yyyy")
    calendario.pack(pady=20)

    # Podés agregar más elementos aquí, como recordatorios o mensajes