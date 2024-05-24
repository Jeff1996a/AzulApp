import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image

from TipoPrenda.FrmActualizarPrendaCatalogo import FrmActualizarPrendaCatalogo
from dbConnection import dbConnection


class FrmCatalogoPrendas(tk.Toplevel):
    def __init__(self, datos_usuario):
        super().__init__()
        self.datos_usuario = datos_usuario
        self.catalogo_prendas = []

        # Conexión a la base de datos Azul lavandería
        self.db = dbConnection()
        self.cnx = self.db.cnx

        # ******************************************TITULO DEL FORMULARIO**********************************
        self.lblTitulo = ttk.Label(self, text='Azul Lavandería', font=('Courier', 20), foreground='blue')
        self.lblTitulo.pack(side='top', padx=20, pady=5)

        # Subtitulo del formulario
        self.label_subtitulo = ttk.Label(self, text='Catálogo de prendas', font=('Courier', 15),
                                         foreground='purple')
        self.label_subtitulo.pack(side='top', anchor='center', padx=15, pady=5)

        # ***************************************CONTENEDOR AGREGAR NUEVA PRENDA ******************************
        self.frm_agregar_prenda = tk.LabelFrame(self, text='AGREGAR NUEVA PRENDA', font=("Courier", 12),
                                                foreground='green')
        self.frm_agregar_prenda.pack(side='top', fill='both', padx=5, pady=5)

        self.descripcion_servicios = []
        self.servicios = []

        self.obtener_servicios()

        for servicio in self.servicios:
            self.descripcion_servicios.append(servicio[1])

        # Label ingresar prenda
        self.label_descripcion = ttk.Label(self.frm_agregar_prenda, text='Tipo de prenda: ')
        self.label_descripcion.grid(row=0, column=0, padx=0, pady=0)

        self.descripcion_prenda  = tk.StringVar()

        # Text ingresar prenda
        self.txt_descripcion = ttk.Entry(self.frm_agregar_prenda, width=40, textvariable=self.descripcion_prenda)
        self.txt_descripcion.grid(row=0, column=1, padx=5, pady=0)

        self.descripcion_prenda.trace('w', self.upper_descripcion())

        # Botón agregar tipo de prenda
        # Create an object of tkinter ImageTk
        self.addImg = Image.open("Img/add.png")
        self.newAddImg = self.addImg.resize((15, 15))
        self.add = ImageTk.PhotoImage(self.newAddImg)

        self.button_agregar = ttk.Button(self.frm_agregar_prenda,
                                         text='Agregar',
                                         image=self.add,
                                         compound='right',
                                         command=self.agregar_prenda
                                         )
        self.button_agregar.grid(row=0, column=3, padx=5, pady=0)

        # Label tipo de servicio
        self.label_tipo_serv = ttk.Label(self.frm_agregar_prenda, text='Tipo de servicio:')
        self.label_tipo_serv.grid(sticky='nw', row=1, column=0, padx=0, pady=3)

        self.tipo_servicio = tk.StringVar()

        # Text tipo servicio
        self.combo_tipo_serv = ttk.Combobox(self.frm_agregar_prenda, width=20,
                                            values=self.descripcion_servicios, textvariable=self.tipo_servicio)
        self.combo_tipo_serv.grid(sticky='nw', row=1, column=1, padx=5, pady=3)

        # Label precio
        self.label_precio = ttk.Label(self.frm_agregar_prenda, text='Precio ($):')
        self.label_precio.grid(sticky='nw', row=2, column=0, padx=0, pady=3)

        self.precio = tk.DoubleVar()

        # Text precio
        self.txt_precio = ttk.Entry(self.frm_agregar_prenda, width=20, textvariable=self.precio)
        self.txt_precio.grid(sticky='nw', row=2, column=1, padx=5, pady=3)

        # *****************************************CONTENEDOR TABLA**********************************************
        # Contenedor principal
        self.contenedor_catalogo = tk.LabelFrame(self, text='LISTADO DE PRENDAS Y PRECIOS', font=("Courier", 12),
                                                  foreground='green')
        self.contenedor_catalogo.pack(side='top', fill='both', padx=5, pady=5)

        # **************************************** BUSCAR TIPO DE PRENDA ********************************************
        self.contenedor_buscar = tk.Frame(self.contenedor_catalogo)
        self.contenedor_buscar.pack(side='top', fill='both')

        self.buscar = tk.StringVar()

        self.label_buscar = ttk.Label(self.contenedor_buscar, text='Buscar: ', font=("Courier", 10),
                                      foreground='gray')
        self.label_buscar.pack(side='left', fill='both', padx=5, pady=0)

        self.txt_buscar_producto = ttk.Entry(self.contenedor_buscar, width=40, textvariable=self.buscar)
        self.txt_buscar_producto.pack(side='left', fill='both')

        self.buscar.trace('w', self.obtener_prendas)

        # *************************************** TABLA DE PRENDAS *************************************************
        self.contenedor_tabla = tk.Frame(self.contenedor_catalogo)
        self.contenedor_tabla.pack(side='top', fill='both')

        # Treeview para el catálogo de productos
        self.encabezado_catalogo = ('#1', '#2', '#3', '#4')
        self.tabla_catalogo = ttk.Treeview(self.contenedor_tabla, columns=self.encabezado_catalogo, show='headings')
        self.tabla_catalogo.pack(side='top', fill='both', padx=5, pady=5)

        self.context_menu = tk.Menu(self.tabla_catalogo, tearoff=0)
        self.context_menu.add_command(label="Eliminar prenda", command=self.eliminar_prenda)
        self.context_menu.add_command(label="Actualizar datos", command=self.actualizar_prenda)

        self.tabla_catalogo.bind("<Button-3>", self.popup)

        self.tabla_catalogo.column('#1', width=25, minwidth=25, stretch=False, anchor='center')
        self.tabla_catalogo.column('#2', width=230, minwidth=230, stretch=False)
        self.tabla_catalogo.column('#3', width=80, minwidth=80, stretch=False, anchor='center')
        self.tabla_catalogo.column('#4', width=100, minwidth=100, stretch=False, anchor='center')

        self.tabla_catalogo.heading('#1', text="N°", anchor='center')
        self.tabla_catalogo.heading('#2', text='DESCRIPCIÓN', anchor='center')
        self.tabla_catalogo.heading('#3', text='PRECIO ($)', anchor='center')
        self.tabla_catalogo.heading('#4', text='SERVICIO', anchor='center')

        self.obtener_prendas()

        self.focus()
        self.grab_set()

    def agregar_prenda(self):

        if self.cnx.is_connected():

            servicio = self.tipo_servicio.get()
            id_servicio = 0

            if servicio == 'SECO':
                id_servicio = 1
            elif servicio == 'LOCAL':
                id_servicio = 2
            elif servicio == 'PRODUCTO':
                id_servicio = 3
            elif servicio == 'TINTURADO':
                id_servicio = 4
            elif servicio == 'PLANTA AZUL':
                id_servicio = 5

            if self.precio.get() == 0:
                messagebox.showerror(message='INGRESAR EL PRECIO DE LAVADO', title='Agregar prenda a catálogo')
            elif self.descripcion_prenda.get() == '':
                messagebox.showerror(message='INGRESAR LA DESCRIPCIÓN DE LA PRENDA', title='Agregar prenda a catálogo')
            elif self.tipo_servicio.get() == '':
                messagebox.showerror(message='SELECCIONAR EL TIPO DE SERVICIO', title='Agregar prenda a catálogo')
            else:
                cursor = self.cnx.cursor()

                arguments = [self.descripcion_prenda.get(), self.precio.get(), id_servicio]
                print(arguments)
                cursor.callproc('spAgregarTipoPrenda', arguments)

                response = []

                for result in cursor.stored_results():
                    response = result.fetchall()
                    print(response)

                self.cnx.commit()

                id_prenda = response[0][0]

                if id_prenda != 0:
                    messagebox.showinfo(message='PRENDA AGREGADA EXITOSAMENTE!!', title='Agregar prenda a catálogo')
                    self.obtener_prendas()
                    self.descripcion_prenda.set('')
                    self.combo_tipo_serv.set('')
                    self.precio.set(0)
                else:
                    messagebox.showerror(message='NO SE PUDO AGREGAR LA PRENDA', title='Agregar prenda a catálogo')

        else:
            print("Connection failure")


    def eliminar_prenda(self):
        # Get selected item to Delete
        producto = self.tabla_catalogo.focus()
        print(producto)

        selected_item = self.tabla_catalogo.selection()[0]
        details = self.tabla_catalogo.item(selected_item)

        datos_producto = details.get('values')

        print(datos_producto)

        if self.cnx.is_connected():
            print(".....ACTUALIZANDO DATOS PRODUCTO.....")

            cursor = self.cnx.cursor()

            # To pass the input Arguments create a list and pass it
            args = [datos_producto[0]]
            cursor.callproc('spEliminarTipoPrenda', args)

            for result in cursor.stored_results():
                response = result.fetchall()
                print(response)

            # Ejecutar el proceso almacenadoe
            self.cnx.commit()

            if cursor.rowcount != 0:
                self.catalogo_prendas.pop(int(selected_item) - 1)

                self.tabla_catalogo.delete(selected_item)

                messagebox.showinfo(message='PRENDA ELIMINADA CORRECTAMENTE!!', title='Eliminar prenda del catálogo')
                self.obtener_prendas()
        else:
            print("Connection failure")

    def actualizar_prenda(self):
        # Get selected item to Update
        producto = self.tabla_catalogo.focus()
        print(producto)

        selected_item = self.tabla_catalogo.selection()[0]
        details = self.tabla_catalogo.item(selected_item)

        datos_producto = details.get('values')

        frm_actualizar_prenda = FrmActualizarPrendaCatalogo(self.datos_usuario, datos_producto)

        self.destroy()

    def obtener_prendas(self, *args):

        texto_buscar = self.buscar.get()

        # Limpiar la tabla
        for i in self.tabla_catalogo.get_children():
            self.tabla_catalogo.delete(i)

        if self.cnx.is_connected():
            if texto_buscar == '':

                print(".....OBTENIENDO PRENDAS DEL CATÁLOGO.....")

                cursor = self.cnx.cursor()

                # Llama al proceso almacenado
                cursor.callproc('spObtenerPrendas')

                for result in cursor.stored_results():
                    self.catalogo_prendas = result.fetchall()
                    print(self.catalogo_prendas)

                i = 1
                for prenda in self.catalogo_prendas:
                    self.tabla_catalogo.insert("", 'end', iid=i, values=prenda)
                    i += 1

                self.cnx.commit()

            else:
                print(".....OBTENIENDO PRENDAS DEL CATÁLOGO.....")

                cursor = self.cnx.cursor()

                argument = [texto_buscar]
                # Llama al proceso almacenado
                cursor.callproc('spFiltrarCatalogo', argument)

                for result in cursor.stored_results():
                    self.catalogo_prendas = result.fetchall()
                    print(self.catalogo_prendas)

                i = 1
                for prenda in self.catalogo_prendas:
                    self.tabla_catalogo.insert("", 'end', iid=i, values=prenda)
                    i += 1

                self.cnx.commit()
        else:
            print("Connection failure")

    # Menú para eliminar o editar prendas
    def popup(self, event):
        """action in event of button 3 on tree view"""
        # select row under mouse
        iid = self.tabla_catalogo.identify_row(event.y)
        if iid:
            # mouse pointer over item
            self.tabla_catalogo.selection_set(iid)
            self.context_menu.post(event.x_root, event.y_root)
        else:
            # mouse pointer not over item
            # occurs when items do not fill frame
            # no action required
            pass

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

                # Ejecutar el proceso almacenadoe
                self.cnx.commit()

            else:
                print("Connection failure")

    def upper_descripcion(self, *args):
        self.descripcion_prenda.set(self.descripcion_prenda.get().upper())  # change to Upper case