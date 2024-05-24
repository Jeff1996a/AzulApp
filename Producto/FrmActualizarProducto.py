import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image

from dbConnection import dbConnection


class FrmActualizarProducto(tk.Toplevel):
    def __init__(self, datos_usuario, datos_producto):
        super().__init__()
        self.datos_usuario = datos_usuario
        self.datos_producto = datos_producto

        print(datos_producto)

        # Conexión a la base de datos Azul lavandería
        self.db = dbConnection()
        self.cnx = self.db.cnx

        self.lblTitulo = ttk.Label(self, text='Azul Lavandería', font=('Courier', 20), foreground='blue')
        self.lblTitulo.pack(side='top', padx=20, pady=5)

        # Subtitulo del formulario
        self.label_subtitulo = ttk.Label(self, text='Actualizar producto de inventario ', font=('Courier', 15),
                                         foreground='purple')
        self.label_subtitulo.pack(side='top', anchor='center', padx=15, pady=5)

        # **********************************************CONTENEDOR DESCRIPCION**************************************************
        # Contenedor formulario agregar producto
        self.frm_actualizar_producto = tk.LabelFrame(self, text='DATOS DEL PRODUCTO', font=("Courier", 12),
                                                  foreground='green')
        self.frm_actualizar_producto.pack(side='top', fill='both', padx=10, pady=5)

        # *******************************************CONTENEDOR ID PRODUCTO***********************************************
        # Contenedor para el id el cliente
        self.id_container = tk.Frame(self.frm_actualizar_producto)
        self.id_container.pack(side="top", fill='both')

        self.id_producto = tk.IntVar()

        # Label nombres del cliente
        self.label_id = ttk.Label(self.id_container, text='CÓDIGO:', font=("Courier", 10), width=15)
        self.label_id.pack(side='left', anchor='nw', padx=0, pady=4, ipadx=4, ipady=4)

        # Text nombres del cliente
        self.txt_id = ttk.Entry(self.id_container, width=10, textvariable=self.id_producto)
        self.txt_id.pack(side='left', padx=0, pady=5, ipadx=0, ipady=4)
        self.txt_id.config(state='readonly')

        self.id_producto.set(self.datos_producto[0])

        # ****************************************************CONTENEDOR DESCRIPCION*****************************
        self.descripcion = tk.StringVar()

        # Contenedor para la descripción del producto
        self.contenedor_descripcion = tk.Frame(self.frm_actualizar_producto)
        self.contenedor_descripcion.pack(side="top", fill='both')

        # Label descripción del producto
        self.label_descripcion = ttk.Label(self.contenedor_descripcion, text='DESCRIPCIÓN:', font=("Courier", 10),
                                           width=15)
        self.label_descripcion.pack(side='left', anchor='nw', padx=0, pady=4, ipadx=4, ipady=4)

        # Text descripción del producto
        self.txt_descripcion = ttk.Entry(self.contenedor_descripcion, width=30, textvariable=self.descripcion)
        self.txt_descripcion.pack(side='left', padx=0, pady=5, ipadx=2, ipady=2)

        self.descripcion.set(self.datos_producto[1])

        self.descripcion.trace('w', self.upper_descripcion)

        # ********************************************CONTENEDOR CANTIDAD ****************************************
        self.contenedor_cantidad = ttk.Frame(self.frm_actualizar_producto)
        self.contenedor_cantidad.pack(side='top', fill='both')

        self.cantidad = tk.IntVar()

        # Label cantidad de productos
        self.label_cantidad_productos = ttk.Label(self.contenedor_cantidad, text='CANTIDAD: ', font=("Courier", 10),
                                                  width=15)
        self.label_cantidad_productos.pack(side='left', fill='both', padx=0, pady=4, ipadx=4, ipady=4)

        # Entry cantidad de productos
        self.txt_cantidad_productos = ttk.Entry(self.contenedor_cantidad, width=15, textvariable=self.cantidad)
        self.txt_cantidad_productos.pack(side='left', ipadx=2, ipady=2, padx=0, pady=0)

        self.cantidad.set(self.datos_producto[2])

        # ********************************************CONTENEDOR STOCK ****************************************
        self.contenedor_stock = ttk.Frame(self.frm_actualizar_producto)
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

        self.opcion.set(self.datos_producto[3])

        # ******************************************** CONTENEDOR PRECIO ****************************************
        self.contenedor_precio = ttk.Frame(self.frm_actualizar_producto)
        self.contenedor_precio.pack(side='top', fill='both')

        self.precio = tk.DoubleVar()

        # Label precio producto
        self.label_precio = ttk.Label(self.contenedor_precio, text='PRECIO ($): ', font=("Courier", 10),
                                      width=15)
        self.label_precio.pack(side='left', fill='both', padx=0, pady=4, ipadx=4, ipady=4)

        # Entry precio del producto
        self.txt_precio = ttk.Entry(self.contenedor_precio, width=15, textvariable=self.precio)
        self.txt_precio.pack(side='left', ipadx=2, ipady=2, padx=0, pady=0)

        self.precio.set(self.datos_producto[4])

        # ********************************************* CONTENEDOR OBSERVACION *************************************
        # Contenedor observacion del producto
        self.contenedor_observacion = tk.Frame(self.frm_actualizar_producto)
        self.contenedor_observacion.pack(side="top", fill='both')

        self.observacion = tk.StringVar()

        # Label observacion del producto
        self.label_observacion = ttk.Label(self.contenedor_observacion, text='OBSERVACIÓN:', font=("Courier", 10),
                                           width=15)
        self.label_observacion.pack(side='left', anchor='nw', padx=0, pady=4, ipadx=4, ipady=4)

        # Entry observacion del producto
        self.txt_observacion = ttk.Entry(self.contenedor_observacion, width=30, textvariable=self.observacion)
        self.txt_observacion.pack(side='left', padx=0, pady=5, ipadx=2, ipady=2)

        self.observacion.set(self.datos_producto[5])

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
            command=self.actualizar_producto,
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

    def actualizar_producto(self):

        if self.cnx.is_connected():
            print(".....ACTUALIZANDO DATOS PRODUCTO.....")

            cursor = self.cnx.cursor()

            # To pass the input Arguments create a list and pass it
            args = [self.id_producto.get(), self.descripcion.get(), self.cantidad.get(), self.opcion.get(),
                    self.precio.get(), self.observacion.get()]
            cursor.callproc('spActualizarProducto', args)

            for result in cursor.stored_results():
                response = result.fetchall()
                print(response)

            # Ejecutar el proceso almacenadoe
            self.cnx.commit()

            if cursor.rowcount != 0:
                messagebox.showinfo(message='PRODUCTO ACTUALIZADO CORRECTAMENTE!!', title='Entregar pedido')
                self.destroy()
        else:
            print("Connection failure")

    def upper_descripcion(self, *args):
        self.descripcion.set(self.descripcion.get().upper())  # change to Upper case

    def upper_observacion(self, *args):
        self.observacion.set(self.observacion.get().upper())  # change to Upper case