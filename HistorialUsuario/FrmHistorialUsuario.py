import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image

from Producto.FrmActualizarProducto import FrmActualizarProducto
from Producto.FrmAgregarProducto import FrmAgregarProducto
from dbConnection import  dbConnection


class FrmHistorialUsuario(tk.Toplevel):
    def __init__(self, datos_usuario):
        super().__init__()

        # Datos del usuario conectado
        self.datos_usuario = datos_usuario

        # Registro de usuarios
        self.registro_usuario = []

        # ******************************************TITULO DEL FORMULARIO**********************************
        self.lblTitulo = ttk.Label(self, text='Azul Lavandería', font=('Courier', 20), foreground='blue')
        self.lblTitulo.pack(side='top', padx=20, pady=5)

        # Subtitulo del formulario
        self.label_subtitulo = ttk.Label(self, text='Registro de asistencia', font=('Courier', 15),
                                         foreground='purple')
        self.label_subtitulo.pack(side='top', anchor='center', padx=15, pady=5)

        # *****************************************CONTENEDOR PRINCIPAL**********************************************
        # Contenedor principal
        self.contenedor_ordenes = tk.LabelFrame(self, text='REGISTRO DE PRENDAS POR RETIRAR', font=("Courier", 12),
                                                foreground='green')
        self.contenedor_ordenes.pack(side='top', fill='both', padx=5, pady=5)


