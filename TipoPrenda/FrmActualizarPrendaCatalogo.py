import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image

from dbConnection import dbConnection


class FrmActualizarPrendaCatalogo(tk.Toplevel):
    def __init__(self, datos_usuario, datos_prenda):
        super().__init__()
        self.datos_usuario = datos_usuario
        self.datos_prenda = datos_prenda

        print(datos_prenda)

        # Conexión a la base de datos Azul lavandería
        self.db = dbConnection()
        self.cnx = self.db.cnx

        self.lblTitulo = ttk.Label(self, text='Azul Lavandería', font=('Courier', 20), foreground='blue')
        self.lblTitulo.pack(side='top', padx=20, pady=5)

        # Subtitulo del formulario
        self.label_subtitulo = ttk.Label(self, text='Actualizar prenda del catálogo ', font=('Courier', 15),
                                         foreground='purple')
        self.label_subtitulo.pack(side='top', anchor='center', padx=15, pady=5)

        # **********************************************CONTENEDOR DESCRIPCION**************************************************
        # Contenedor formulario agregar producto
        self.frm_actualizar_prenda = tk.LabelFrame(self, text='DATOS DE LA PRENDA/ACCESORIO', font=("Courier", 12),
                                                  foreground='green')
        self.frm_actualizar_prenda.pack(side='top', fill='both', padx=10, pady=5)

        # *******************************************CONTENEDOR ID PRODUCTO***********************************************
        # Contenedor para el id el cliente
        self.id_container = tk.Frame(self.frm_actualizar_prenda)
        self.id_container.pack(side="top", fill='both')

        self.id_prenda = tk.IntVar()

        # Label nombres del cliente
        self.label_id = ttk.Label(self.id_container, text='CÓDIGO:', font=("Courier", 10), width=20)
        self.label_id.pack(side='left', anchor='nw', padx=0, pady=4, ipadx=4, ipady=4)

        # Text nombres del cliente
        self.txt_id = ttk.Entry(self.id_container, width=10, textvariable=self.id_prenda)
        self.txt_id.pack(side='left', padx=0, pady=5, ipadx=0, ipady=4)
        self.txt_id.config(state='readonly')

        self.id_prenda.set(self.datos_prenda[0])

        # ****************************************************CONTENEDOR DESCRIPCION*****************************
        self.descripcion = tk.StringVar()

        # Contenedor para la descripción del producto
        self.contenedor_descripcion = tk.Frame(self.frm_actualizar_prenda)
        self.contenedor_descripcion.pack(side="top", fill='both')

        # Label descripción del producto
        self.label_descripcion = ttk.Label(self.contenedor_descripcion, text='DESCRIPCIÓN:', font=("Courier", 10),
                                           width=20)
        self.label_descripcion.pack(side='left', anchor='nw', padx=0, pady=4, ipadx=4, ipady=4)

        # Text descripción del producto
        self.txt_descripcion = ttk.Entry(self.contenedor_descripcion, width=30, textvariable=self.descripcion)
        self.txt_descripcion.pack(side='left', padx=0, pady=5, ipadx=2, ipady=2)

        self.descripcion.set(self.datos_prenda[1])

        self.descripcion.trace('w', self.upper_descripcion)

        # ********************************************CONTENEDOR TIPO DE SERVICIO ****************************************
        # Contenedor tipo de servicio
        self.contenedor_servicio = tk.Frame(self.frm_actualizar_prenda)
        self.contenedor_servicio.pack(side='top', fill='both')

        self.descripcion_servicios = []
        self.servicios = []

        self.obtener_servicios()

        for servicio in self.servicios:
            self.descripcion_servicios.append(servicio[1])

        # Label tipo de servicio
        self.label_tipo_serv = ttk.Label(self.contenedor_servicio, text='TIPO DE SERVICIO:', font=("Courier", 10),
                                           width=20)
        self.label_tipo_serv.pack(side='left', anchor='nw', padx=0, pady=4, ipadx=4, ipady=4)

        self.tipo_servicio = tk.StringVar()

        # Text tipo servicio
        self.combo_tipo_serv = ttk.Combobox(self.contenedor_servicio, width=20,
                                            values=self.descripcion_servicios, textvariable=self.tipo_servicio)
        self.combo_tipo_serv.pack(side='left', padx=0, pady=5, ipadx=2, ipady=2)

        self.tipo_servicio.set(datos_prenda[3])

        # ******************************************** CONTENEDOR PRECIO ****************************************
        self.contenedor_precio = ttk.Frame(self.frm_actualizar_prenda)
        self.contenedor_precio.pack(side='top', fill='both')

        self.precio = tk.DoubleVar()

        # Label precio producto
        self.label_precio = ttk.Label(self.contenedor_precio, text='PRECIO ($): ', font=("Courier", 10),
                                      width=20)
        self.label_precio.pack(side='left', fill='both', padx=0, pady=4, ipadx=4, ipady=4)

        # Entry precio del producto
        self.txt_precio = ttk.Entry(self.contenedor_precio, width=15, textvariable=self.precio)
        self.txt_precio.pack(side='left', ipadx=2, ipady=2, padx=0, pady=0)

        self.precio.set(self.datos_prenda[2])


        # ****************************************** BOTONES PARA ACTUALIZAR Y CERRAR ****************************************

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
            command=self.actualizar_prenda,
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

    def actualizar_prenda(self):

        tipo_servicio = self.tipo_servicio.get()
        id_servicio = 0

        if tipo_servicio == 'SECO':
            id_servicio = 1
        elif tipo_servicio == 'LOCAL':
            id_servicio = 2
        elif tipo_servicio == 'PRODUCTO':
            id_servicio = 3
        elif tipo_servicio == 'TINTURADO':
            id_servicio = 4
        elif tipo_servicio == 'PLANTA AZUL':
            id_servicio = 5

        if self.cnx.is_connected():
            print(".....ACTUALIZANDO DATOS PRODUCTO.....")

            cursor = self.cnx.cursor()

            # To pass the input Arguments create a list and pass it
            args = [self.id_prenda.get(), self.descripcion.get(), id_servicio,
                    self.precio.get()]
            cursor.callproc('spActualizarTipoPrenda', args)

            for result in cursor.stored_results():
                response = result.fetchall()
                print(response)

            # Ejecutar el proceso almacenadoe
            self.cnx.commit()

            if cursor.rowcount != 0:
                messagebox.showinfo(message='PRENDA ACTUALIZADA CORRECTAMENTE!!', title='Entregar pedido')
                self.destroy()
        else:
            print("Connection failure")

    # Función para obtener el tipo de servicio
    def obtener_servicios(self):

        lista_servicios = []

        if self.cnx.is_connected():

            print("Esperando para obtener prendas")

            cursor = self.cnx.cursor()

            # Llama al proceso almacenado
            cursor.callproc('spObtenerServicios')

            for result in cursor.stored_results():
                lista_servicios = result.fetchall()
                print(lista_servicios)

            i = 1

            self.servicios = []

            for servicio in lista_servicios:
                self.servicios.append(servicio)
                print(self.servicios)

            # Ejecutar el proceso almacenado
            self.cnx.commit()

        else:
            print("Connection failure")

    def upper_descripcion(self, *args):
        self.descripcion.set(self.descripcion.get().upper())  # change to Upper case
