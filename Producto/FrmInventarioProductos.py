import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image

from Producto.FrmActualizarProducto import FrmActualizarProducto
from Producto.FrmAgregarProducto import FrmAgregarProducto
from dbConnection import  dbConnection

class FrmInventarioProductos(tk.Toplevel):
    def __init__(self, datos_usuario):
        super().__init__()
        self.datos_usuario = datos_usuario

        self.productos_inventario = []

        # ******************************************TITULO DEL FORMULARIO**********************************
        self.lblTitulo = ttk.Label(self, text='Azul Lavandería', font=('Courier', 20), foreground='blue')
        self.lblTitulo.pack(side='top', padx=20, pady=5)

        # Subtitulo del formulario
        self.label_subtitulo = ttk.Label(self, text='Inventario de productos ', font=('Courier', 15),
                                         foreground='purple')
        self.label_subtitulo.pack(side='top', anchor='center', padx=15, pady=5)

        # *****************************************CONTENEDOR PRINCIPAL**********************************************
        # Contenedor principal
        self.contenedor_productos = tk.LabelFrame(self,  text='REGISTRO DE PRODUCTOS', font=("Courier", 12),
                                                 foreground='green')
        self.contenedor_productos.pack(side='top', fill='both', padx=5, pady=5)

        # *****************************************CONTENEDOR BUSCAR PRODUCTOS ***********************************************
        self.contenedor_buscar = tk.Frame(self.contenedor_productos)
        self.contenedor_buscar.pack(side='top', fill='both')

        self.buscar = tk.StringVar()

        self.label_buscar = ttk.Label(self.contenedor_buscar, text='Buscar: ', font=("Courier", 10),
                                      foreground='gray')
        self.label_buscar.pack(side='left', fill='both', padx=5, pady=0)

        self.txt_buscar_producto = ttk.Entry(self.contenedor_buscar, width=50, textvariable=self.buscar)
        self.txt_buscar_producto.pack(side='left', fill='both')

        self.buscar.trace('w', self.obtener_productos)

        # Create an object of tkinter ImageTk
        self.addImg = Image.open("Img/add.png")
        self.newAddImg = self.addImg.resize((15, 15))
        self.add = ImageTk.PhotoImage(self.newAddImg)

        self.button_agregar = ttk.Button(self.contenedor_buscar,
                                         text='Agregar',
                                         image=self.add,
                                         compound='right',
                                         command=self.agregar_producto
                                         )
        self.button_agregar.pack(side='right', fill='both', padx=5, pady=0)

        # **********************************************CONTENEDOR TABLA PRENDAS**************************************
        self.contenedor_tabla = tk.Frame(self.contenedor_productos)
        self.contenedor_tabla.pack(side='top', fill='both')

        # Treeview para los productos del inventario
        self.encabezado = ('#1', '#2', '#3', '#4', '#5', '#6')
        self.tabla_productos = ttk.Treeview(self.contenedor_tabla, columns=self.encabezado, show='headings')
        self.tabla_productos.pack(side='bottom', fill='both', padx=5, pady=5)

        self.context_menu = tk.Menu(self.tabla_productos, tearoff=0)
        self.context_menu.add_command(label="Eliminar producto de inventario", command=self.eliminar_producto)
        self.context_menu.add_command(label="Actualizar datos del producto", command=self.actualizar_producto)

        self.tabla_productos.bind("<Button-3>", self.popup)

        self.tabla_productos.column('#1', width=25, minwidth=25, stretch=False, anchor='center')
        self.tabla_productos.column('#2', width=180, minwidth=180, stretch=False)
        self.tabla_productos.column('#3', width=80, minwidth=80, stretch=False, anchor='center')
        self.tabla_productos.column('#4', width=80, minwidth=80, stretch=False, anchor='center')
        self.tabla_productos.column('#5', width=80, minwidth=80, stretch=False, anchor='center')
        self.tabla_productos.column('#6', width=100, minwidth=100, stretch=False)

        self.tabla_productos.heading('#1', text="N°", anchor='center')
        self.tabla_productos.heading('#2', text='DESCRIPCION')
        self.tabla_productos.heading('#3', text='CANTIDAD', anchor='center')
        self.tabla_productos.heading('#4', text='STOCK', anchor='center')
        self.tabla_productos.heading('#5', text='PRECIO ($)', anchor='center')
        self.tabla_productos.heading('#6', text='OBSERVACIÓN')

        self.obtener_productos()

        # *****CONTENEDOR BOTONES******
        self.button_container = tk.Frame(self)
        self.button_container.pack(side="bottom")

        # Create an object of tkinter ImageTk
        self.printImg = Image.open("Img/print.png")
        self.newPrintImg = self.printImg.resize((15, 15))
        self.print = ImageTk.PhotoImage(self.newPrintImg)

        # Botón para guardar los datos
        self.imprimir_button = ttk.Button(
            self.button_container,
            text="IMPRIMIR",
            image=self.print,
            compound='right',
        )
        self.imprimir_button.pack(side='left', anchor='center', padx=10, pady=10, ipadx=5, ipady=2)

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

    def obtener_productos(self, *args):

        # Conexión a la base de datos Azul lavandería
        db = dbConnection()
        cnx = db.cnx

        texto = self.buscar.get()

        # Limpiar la tabla
        for i in self.tabla_productos.get_children():
            self.tabla_productos.delete(i)

        if cnx.is_connected():
            if texto == '':
                print(".....OBTENIENDO INFORMACIÓN DE LA ORDEN DE TRABAJO.....")

                cursor = cnx.cursor()

                # Llama al proceso almacenado
                cursor.callproc('spObtenerProductos')

                for result in cursor.stored_results():
                    self.productos_inventario = result.fetchall()
                    print(self.productos_inventario)

                i = 1
                for producto in self.productos_inventario:
                    self.tabla_productos.insert("", 'end', iid=i, values=producto)
                    i += 1

                cnx.commit()

                cursor.close()
                cnx.close()

            else:
                print(".....OBTENIENDO INFORMACIÓN DE LA ORDEN DE TRABAJO.....")

                cursor = cnx.cursor()

                # Llama al proceso almacenado
                argumento = [texto]
                cursor.callproc('spFiltrarProductos', argumento)

                for result in cursor.stored_results():
                    self.productos_inventario = result.fetchall()
                    print(self.productos_inventario)

                i = 1
                for producto in self.productos_inventario:
                    self.tabla_productos.insert("", 'end', iid=i, values=producto)
                    i += 1

                cnx.commit()

                cursor.close()
                cnx.close()
        else:
            print("Connection failure")

    def agregar_producto(self):
        frm_agregar_producto = FrmAgregarProducto(self.datos_usuario)
        self.destroy()

    def eliminar_producto(self):

        # Conexión a la base de datos Azul lavandería
        db = dbConnection()
        cnx = db.cnx

        # Get selected item to Delete
        producto = self.tabla_productos.focus()
        print(producto)

        selected_item = self.tabla_productos.selection()[0]
        details = self.tabla_productos.item(selected_item)

        datos_producto = details.get('values')

        print(datos_producto)

        if cnx.is_connected():
            print(".....ACTUALIZANDO DATOS PRODUCTO.....")

            cursor = cnx.cursor()

            # To pass the input Arguments create a list and pass it
            args = [datos_producto[0]]
            cursor.callproc('spEliminarProducto', args)

            for result in cursor.stored_results():
                response = result.fetchall()
                print(response)

            # Ejecutar el proceso almacenadoe
            cnx.commit()

            if cursor.rowcount != 0:
                self.productos_inventario.pop(int(selected_item) - 1)

                self.tabla_productos.delete(selected_item)

                messagebox.showinfo(message='PRODUCTO ELIMINADO CORRECTAMENTE!!', title='Eliminar producto')
                self.obtener_productos()

            cursor.close()
            cnx.close()

        else:
            print("Connection failure")

    def actualizar_producto(self):
        # Get selected item to Update
        producto = self.tabla_productos.focus()
        print(producto)

        selected_item = self.tabla_productos.selection()[0]
        details = self.tabla_productos.item(selected_item)

        datos_producto = details.get('values')

        frm_actualizar_producto = FrmActualizarProducto(self.datos_usuario, datos_producto)

        self.destroy()

    # Menú para eliminar o editar prendas
    def popup(self, event):
        """action in event of button 3 on tree view"""
        # select row under mouse
        iid = self.tabla_productos.identify_row(event.y)
        if iid:
            # mouse pointer over item
            self.tabla_productos.selection_set(iid)
            self.context_menu.post(event.x_root, event.y_root)
        else:
            # mouse pointer not over item
            # occurs when items do not fill frame
            # no action required
            pass