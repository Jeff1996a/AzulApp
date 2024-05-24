import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image

from dbConnection import dbConnection
class FrmAgregarProducto(tk.Toplevel):

    def __init__(self, datos_usuario):
        super().__init__()
        self.datos_usuario = datos_usuario

        # Conexión a la base de datos Azul lavandería
        self.db = dbConnection()
        self.cnx = self.db.cnx

        self.lblTitulo = ttk.Label(self, text='Azul Lavandería', font=('Courier', 20), foreground='blue')
        self.lblTitulo.pack(side='top', padx=20, pady=5)

        # Subtitulo del formulario
        self.label_subtitulo = ttk.Label(self, text='Agregar producto a inventario ', font=('Courier', 15), foreground='purple')
        self.label_subtitulo.pack(side='top', anchor='center', padx=15, pady=5)

        # **********************************************CONTENEDOR DESCRIPCION**************************************************
        # Contenedor formulario agregar producto
        self.frm_agregar_producto = tk.LabelFrame(self, text='NUEVO PRODUCTO', font=("Courier", 12),
                                               foreground='green')
        self.frm_agregar_producto.pack(side='top', fill='both', padx=10, pady=5)

        self.descripcion = tk.StringVar()

        # Contenedor para la descripción del producto
        self.contenedor_descripcion = tk.Frame(self.frm_agregar_producto)
        self.contenedor_descripcion.pack(side="top", fill='both')

        # Label descripción del producto
        self.label_descripcion = ttk.Label(self.contenedor_descripcion, text='DESCRIPCIÓN:', font=("Courier", 10), width=15)
        self.label_descripcion.pack(side='left', anchor='nw', padx=0, pady=4, ipadx=4, ipady=4)

        # Text descripción del producto
        self.txt_descripcion = ttk.Entry(self.contenedor_descripcion, width=30, textvariable=self.descripcion)
        self.txt_descripcion.pack(side='left', padx=0, pady=5, ipadx=2, ipady=2)

        self.descripcion.trace('w', self.upper_descripcion)

        # ********************************************CONTENEDOR CANTIDAD ****************************************
        self.contenedor_cantidad = ttk.Frame(self.frm_agregar_producto)
        self.contenedor_cantidad.pack(side='top', fill='both')

        self.cantidad = tk.IntVar()

        # Label cantidad de productos
        self.label_cantidad_productos = ttk.Label(self.contenedor_cantidad, text='CANTIDAD: ', font=("Courier", 10),
                                                  width=15)
        self.label_cantidad_productos.pack(side='left', fill='both', padx=0, pady=4, ipadx=4, ipady=4)

        # Entry cantidad de productos
        self.txt_cantidad_productos = ttk.Entry(self.contenedor_cantidad, width=15, textvariable=self.cantidad)
        self.txt_cantidad_productos.pack(side='left', ipadx=2, ipady=2, padx=0, pady=0)

        # ********************************************CONTENEDOR STOCK ****************************************
        self.contenedor_stock = ttk.Frame(self.frm_agregar_producto)
        self.contenedor_stock.pack(side='top', fill='both')

        # Label stock de productos
        self.label_stock = ttk.Label(self.contenedor_stock, text='EN STOCK: ', font=("Courier", 10),
                                                  width=15)
        self.label_stock.pack(side='left', fill='both', padx=0, pady=4, ipadx=4, ipady=4)

        self.opcion = tk.IntVar()

        ttk.Radiobutton(self.contenedor_stock, text="Si", variable=self.opcion, value=1).pack(side='left', padx=0,
                                                                                            pady=0)
        ttk.Radiobutton(self.contenedor_stock, text="No", variable=self.opcion, value=2).pack(side='left',
                                                                                              padx=5, pady=0)

        # ******************************************** CONTENEDOR PRECIO ****************************************
        self.contenedor_precio = ttk.Frame(self.frm_agregar_producto)
        self.contenedor_precio.pack(side='top', fill='both')

        self.precio = tk.DoubleVar()

        # Label precio producto
        self.label_precio = ttk.Label(self.contenedor_precio, text='PRECIO ($): ', font=("Courier", 10),
                                                  width=15)
        self.label_precio.pack(side='left', fill='both', padx=0, pady=4, ipadx=4, ipady=4)

        # Entry precio del producto
        self.txt_precio = ttk.Entry(self.contenedor_precio, width=15, textvariable=self.precio)
        self.txt_precio.pack(side='left', ipadx=2, ipady=2, padx=0, pady=0)

        # ********************************************* CONTENEDOR OBSERVACION *************************************
        # Contenedor observacion del producto
        self.contenedor_observacion = tk.Frame(self.frm_agregar_producto)
        self.contenedor_observacion.pack(side="top", fill='both')

        self.observacion = tk.StringVar()

        # Label observacion del producto
        self.label_observacion = ttk.Label(self.contenedor_observacion, text='OBSERVACIÓN:', font=("Courier", 10),
                                           width=15)
        self.label_observacion.pack(side='left', anchor='nw', padx=0, pady=4, ipadx=4, ipady=4)

        # Entry observacion del producto
        self.txt_observacion = ttk.Entry(self.contenedor_observacion, width=30, textvariable=self.observacion)
        self.txt_observacion.pack(side='left', padx=0, pady=5, ipadx=2, ipady=2)

        self.observacion.trace('w', self.upper_observacion)

        # ****************************************** BOTONES PARA AGREGAR Y CERRAR ****************************************

        # Contenedor para los botones
        self.button_container = tk.Frame(self)
        self.button_container.pack(side="bottom")

        # Create an object of tkinter ImageTk
        self.saveImg = Image.open("Img/save.png")
        self.newSaveImg = self.saveImg.resize((15, 15))
        self.save = ImageTk.PhotoImage(self.newSaveImg)

        # Botón para guardar los datos
        self.guardar_button = ttk.Button(
            self.button_container,
            text="GUARDAR",
            command=self.agregar_producto,
            image=self.save,
            compound='right',
        )
        self.guardar_button.pack(side='left', anchor='center', padx=10, pady=10, ipadx=5, ipady=2)

        # Create an object of tkinter ImageTk
        self.cancelImg = Image.open("Img/cancel.png")
        self.newCancelImg = self.cancelImg.resize((15, 15))
        self.cancel = ImageTk.PhotoImage(self.newCancelImg)

        # Botón para cancelar el registro
        self.cancelar_registro = ttk.Button(
            self.button_container,
            text="CANCELAR",
            command=self.destroy,
            image=self.cancel,
            compound='right',
        )
        self.cancelar_registro.pack(side='right', anchor='center', padx=10, pady=10, ipadx=5, ipady=2)

        self.focus()
        self.grab_set()

    def agregar_producto(self):

        if self.cnx.is_connected():

            print("Esperando para enviar datos")
            cursor = self.cnx.cursor()

            # To pass the input Arguments create a client
            producto = [self.descripcion.get(), self.cantidad.get(), self.opcion.get(), self.precio.get(),
                                self.observacion.get()]
            cursor.callproc('spAgregarProducto', producto)

            result = 0

            for result in cursor.stored_results():
                a = result.fetchall()
                result = a[0]

            # Imprimir la última fila agregada
            id_procucto = result[0]

            # Ejecutar el proceso almacenadoe
            self.cnx.commit()

            if id_procucto == 0:
                messagebox.showerror(message='EL PRODUCTO YA EXISTE EN INVENTARIO',
                                     title='Error de registro')
            else:
                messagebox.showinfo(message='PRODUCTO INGRESADO EXITOSAMENTE',
                                    title='Registro completo')
                self.descripcion.set('')
                self.cantidad.set(0)
                self.opcion.set(0)
                self.precio.set(0)
                self.observacion.set('')

        else:
            print("Connection failure")

    def upper_descripcion(self, *args):
        self.descripcion.set(self.descripcion.get().upper())  # change to Upper case

    def upper_observacion(self, *args):
        self.observacion.set(self.observacion.get().upper())  # change to Upper case