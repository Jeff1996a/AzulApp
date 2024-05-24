import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image

from Producto.FrmActualizarProducto import FrmActualizarProducto
from Producto.FrmAgregarProducto import FrmAgregarProducto
from dbConnection import  dbConnection

class FrmInventarioPrendas(tk.Toplevel):
    def __init__(self, datos_usuario):
        super().__init__()
        self.datos_usuario = datos_usuario

        self.prendas_por_entregar = []

        # Conexión a la base de datos Azul lavandería
        self.db = dbConnection()
        self.cnx = self.db.cnx

        # ******************************************TITULO DEL FORMULARIO**********************************
        self.lblTitulo = ttk.Label(self, text='Azul Lavandería', font=('Courier', 20), foreground='blue')
        self.lblTitulo.pack(side='top', padx=20, pady=5)

        # Subtitulo del formulario
        self.label_subtitulo = ttk.Label(self, text='Inventario de ropa', font=('Courier', 15),
                                         foreground='purple')
        self.label_subtitulo.pack(side='top', anchor='center', padx=15, pady=5)

        # *****************************************CONTENEDOR PRINCIPAL**********************************************
        # Contenedor principal
        self.contenedor_prendas = tk.LabelFrame(self,  text='REGISTRO DE PRENDAS POR RETIRAR', font=("Courier", 12),
                                                 foreground='green')
        self.contenedor_prendas.pack(side='top', fill='both', padx=5, pady=5)

        # *****************************************CONTENEDOR BUSCAR PRODUCTOS ***********************************************
        self.contenedor_buscar = tk.Frame(self.contenedor_prendas)
        self.contenedor_buscar.pack(side='top', fill='both')

        self.label_buscar = ttk.Label(self.contenedor_buscar, text='Buscar: ', font=("Courier", 10),
                                      foreground='gray')
        self.label_buscar.pack(side='left', fill='both', padx=5, pady=0)

        self.txt_buscar_producto = ttk.Entry(self.contenedor_buscar, width=50)
        self.txt_buscar_producto.pack(side='left', fill='both')

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
        self.contenedor_tabla = tk.Frame(self.contenedor_prendas)
        self.contenedor_tabla.pack(side='top', fill='both')

        # Treeview para los productos del inventario
        self.encabezado = ('#1', '#2', '#3', '#4', '#5', '#6', '#7', '#8', '#9', '#10')
        self.tabla_prendas = ttk.Treeview(self.contenedor_tabla, columns=self.encabezado, show='headings')
        self.tabla_prendas.pack(side='bottom', fill='both', padx=5, pady=5)

        self.context_menu = tk.Menu(self.tabla_prendas, tearoff=0)
        self.context_menu.add_command(label="Eliminar", command=self.eliminar_producto)
        self.context_menu.add_command(label="Actualizar", command=self.actualizar_producto)

        self.tabla_prendas.bind("<Button-3>", self.popup)

        self.tabla_prendas.column('#1', width=25, minwidth=25, stretch=False, anchor='center')
        self.tabla_prendas.column('#2', width=80, minwidth=80, stretch=False, anchor='center')
        self.tabla_prendas.column('#3', width=180, minwidth=180, stretch=False, anchor='center')
        self.tabla_prendas.column('#4', width=200, minwidth=200, stretch=False, anchor='center')
        self.tabla_prendas.column('#5', width=100, minwidth=100, stretch=False, anchor='center')
        self.tabla_prendas.column('#6', width=120, minwidth=120, stretch=False, anchor='center')
        self.tabla_prendas.column('#7', width=100, minwidth=100, stretch=False, anchor='center')
        self.tabla_prendas.column('#8', width=100, minwidth=100, stretch=False, anchor='center')
        self.tabla_prendas.column('#9', width=100, minwidth=100, stretch=False, anchor='center')
        self.tabla_prendas.column('#10', width=200, minwidth=200, stretch=False, anchor='center')

        self.tabla_prendas.heading('#1', text="N°", anchor='center')
        self.tabla_prendas.heading('#2', text='NUM. ORDEN', anchor='center')
        self.tabla_prendas.heading('#3', text='CLIENTE', anchor='center')
        self.tabla_prendas.heading('#4', text='DESCRIPCIÓN', anchor='center')
        self.tabla_prendas.heading('#5', text='SERVICIO', anchor='center')
        self.tabla_prendas.heading('#6', text='FECHA ENTREGA', anchor='center')
        self.tabla_prendas.heading('#7', text='ESTADO', anchor='center')
        self.tabla_prendas.heading('#8', text='CANTIDAD', anchor='center')
        self.tabla_prendas.heading('#9', text='TOTAL', anchor='center')
        self.tabla_prendas.heading('#10', text='OBSERVACIONES', anchor='center')

        self.obtener_prendas()

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

    def obtener_prendas(self):

        if self.cnx.is_connected():

            print(".....OBTENIENDO INFORMACIÓN DE LA ORDEN DE TRABAJO.....")

            cursor = self.cnx.cursor()

            # Llama al proceso almacenado
            cursor.callproc('spInventarioPrendas')

            for result in cursor.stored_results():
                self.prendas_por_entregar = result.fetchall()
                print(self.prendas_por_entregar)

            i = 1
            for prenda in self.prendas_por_entregar:
                self.tabla_prendas.insert("", 'end', iid=i, values=prenda)
                i += 1

            self.cnx.commit()
        else:
            print("Connection failure")

    def agregar_producto(self):
        frm_agregar_producto = FrmAgregarProducto(self.datos_usuario)
        self.destroy()

    def eliminar_producto(self):

        # Get selected item to Delete
        producto = self.tabla_prendas.focus()
        print(producto)

        selected_item = self.tabla_prendas.selection()[0]
        details = self.tabla_prendas.item(selected_item)

        datos_producto = details.get('values')

        print(datos_producto)

        if self.cnx.is_connected():
            print(".....ACTUALIZANDO DATOS PRODUCTO.....")

            cursor = self.cnx.cursor()

            # To pass the input Arguments create a list and pass it
            args = [datos_producto[0]]
            cursor.callproc('spEliminarProducto', args)

            for result in cursor.stored_results():
                response = result.fetchall()
                print(response)

            # Ejecutar el proceso almacenadoe
            self.cnx.commit()

            if cursor.rowcount != 0:
                self.prendas_por_entregar.pop(int(selected_item) - 1)

                self.tabla_prendas.delete(selected_item)

                messagebox.showinfo(message='PRODUCTO ELIMINADO CORRECTAMENTE!!', title='Eliminar producto')
                self.obtener_prendas()
        else:
            print("Connection failure")

    def actualizar_producto(self):
        # Get selected item to Update
        producto = self.tabla_prendas.focus()
        print(producto)

        selected_item = self.tabla_prendas.selection()[0]
        details = self.tabla_prendas.item(selected_item)

        datos_producto = details.get('values')

        frm_actualizar_producto = FrmActualizarProducto(self.datos_usuario, datos_producto)

        self.destroy()

    # Menú para eliminar o editar prendas
    def popup(self, event):
        """action in event of button 3 on tree view"""
        # select row under mouse
        iid = self.tabla_prendas.identify_row(event.y)
        if iid:
            # mouse pointer over item
            self.tabla_prendas.selection_set(iid)
            self.context_menu.post(event.x_root, event.y_root)
        else:
            # mouse pointer not over item
            # occurs when items do not fill frame
            # no action required
            pass