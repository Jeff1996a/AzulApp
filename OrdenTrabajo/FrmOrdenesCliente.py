import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
from tkcalendar import *
from datetime import date

from dbConnection import dbConnection

class FrmOrdenesCliente(tk.Toplevel):

    def __init__(self, datos_usuario):
        super().__init__()
        self.datos_usuario = datos_usuario

        # Lista ordenes por cliente
        self.ordenes_cliente = []

        # ****************************** Titulo Principal ****************************
        self.label_titulo = ttk.Label(self, text='Azul Lavandería', font=('Courier', 20), foreground='green')
        self.label_titulo.pack(side='top', anchor='center', padx=10, pady=0)

        # ***************************** Subtítulo ************************************
        self.label_subtitulo = ttk.Label(self, text='Registro de ordenes por cliente', font=('Courier', 15), foreground='purple')
        self.label_subtitulo.pack(side='top', anchor='center', padx=10, pady=5)

        # **************************** Contendor principal *********************************
        self.contenedor_principal = tk.LabelFrame(self, text='CONSULTAR ORDENES', font=('Courier', 15), foreground='green')
        self.contenedor_principal.pack(side='top', fill='both', padx=5, pady=0)

        # ******************************** Contenedor buscar cliente **********************
        self.contenedor_buscar = tk.Frame(self.contenedor_principal)
        self.contenedor_buscar.pack(side='top', anchor='w')

        self.label_buscar = ttk.Label(self.contenedor_buscar, text='Buscar: ', foreground='gray', font=('Courier', 10))
        self.label_buscar.pack(side='left', padx=5, pady=0)

        self.buscar = tk.StringVar()

        self.txt_buscar = ttk.Entry(self.contenedor_buscar, width=35, textvariable=self.buscar)
        self.txt_buscar.pack(side='left', padx=5, pady=0)

        # ********************************** CONTENEDOR TABLA ************************************
        self.contenedor_tabla = tk.Frame(self.contenedor_principal)
        self.contenedor_tabla.pack(side='top')

        self.encabezado = ('#1', '#2', '#3', '#4', '#5', '#6', '#7', '#8', '#9')
        self.tabla_ordenes = ttk.Treeview(self.contenedor_tabla, columns=self.encabezado, show='headings')
        self.tabla_ordenes.pack(side='bottom', fill='both', padx=5, pady=5)

        self.tabla_ordenes.column('#1', width=100, minwidth=100, stretch=False, anchor='center')
        self.tabla_ordenes.column('#2', width=220, minwidth=220, stretch=False)
        self.tabla_ordenes.column('#3', width=100, minwidth=100, stretch=False,anchor='center')
        self.tabla_ordenes.column('#4', width=100, minwidth=100, stretch=False,anchor='center')
        self.tabla_ordenes.column('#5', width=100, minwidth=100, stretch=False,anchor='center')
        self.tabla_ordenes.column('#6', width=100, minwidth=100, stretch=False,anchor='center')
        self.tabla_ordenes.column('#7', width=100, minwidth=100, stretch=False,anchor='center')
        self.tabla_ordenes.column('#8', width=100, minwidth=100, stretch=False,anchor='center')
        self.tabla_ordenes.column('#9', width=180, minwidth=180, stretch=False,anchor='center')

        self.tabla_ordenes.heading('#1', text='NUM. ORDEN')
        self.tabla_ordenes.heading('#2', text='CLIENTE')
        self.tabla_ordenes.heading('#3', text='CÉDULA/RUC')
        self.tabla_ordenes.heading('#4', text='FECHA PEDIDO')
        self.tabla_ordenes.heading('#5', text='ESTADO')
        self.tabla_ordenes.heading('#6', text='FECHA ENTREGA')
        self.tabla_ordenes.heading('#7', text='SALDO ($)')
        self.tabla_ordenes.heading('#8', text='TOTAL ($)')
        self.tabla_ordenes.heading('#9', text='RESPONSABLE')

        self.buscar_orden()
        self.buscar.trace('w', self.buscar_orden)

        self.focus()
        self.grab_set()

    def buscar_orden(self, *args):
        self.ordenes_cliente = []

        # Limpiar la tabla
        for i in self.tabla_ordenes.get_children():
            self.tabla_ordenes.delete(i)

        # Conexión a la base de datos
        db = dbConnection()
        cnx = db.cnx

        if cnx.is_connected():

            cursor = cnx.cursor()

            # Ejecutar consulta
            parametros = [self.buscar.get()]
            cursor.callproc('spObtenerOrdenesPorCliente', parametros)

            ordenes = []

            for result in cursor.stored_results():
                ordenes = result.fetchall()
                print(ordenes)

            i = 0
            for orden in ordenes:
                nueva_orden = [orden[1], orden[2], orden[3], orden[4], orden[5], orden[6], orden[7], orden[8], orden[9]]

                self.tabla_ordenes.insert("", 'end', iid=i,
                                          values=nueva_orden)

                self.ordenes_cliente.append(nueva_orden)

                i += 1

