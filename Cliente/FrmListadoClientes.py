import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

from dbConnection import dbConnection


class ListadoClientes(tk.Toplevel):

    def __init__(self, datos_usuario):

        super().__init__()

        self.datos_usuario = datos_usuario

        self.user_data = []

        self.clientes_registrados = []

        # Imprimir los datos del usuario por consola
        #for arg in args:
            #self.user_data = arg
            #print("argumentos de *argv:", arg)

        self.lblTitulo = ttk.Label(self, text='Azul Lavandería', font=('Courier', 20), foreground='blue')
        self.lblTitulo.pack(side='top', padx=20, pady=5)

        # Pregunta de bienvenida
        self.lblClientesRegistrados = ttk.Label(self, text='Registro de clientes ', font=('Courier', 15), foreground='purple')
        self.lblClientesRegistrados.pack(side='top', anchor='center', padx=15, pady=5)

        # Contenedor lista clientes
        self.frm_lista_clientes = tk.LabelFrame(self, text='CLIENTES REGISTRADOS', font=("Courier", 12),
                                                    foreground='green')
        self.frm_lista_clientes.pack(side='top', fill='both', padx=10, pady=5)

        # Contenedor para el filtro de tablas
        self.contenedor_filtro = tk.Frame(self.frm_lista_clientes)

        # Contenedor para buscar clientes
        self.contenedor_buscar = tk.Frame(self.frm_lista_clientes)
        self.contenedor_buscar.pack(fill='both', side='top', pady=2)

        self.lblBuscar = ttk.Label(self.contenedor_buscar, text='Buscar cliente:', font=('Courier', 10), foreground='gray')
        self.lblBuscar.pack(side='left', anchor='nw', padx=5, pady=2)

        self.txtBuscar = ttk.Entry(self.contenedor_buscar, width=35)
        self.txtBuscar.pack(side='left', anchor='nw', ipadx=0, ipady=0, padx=0, pady=2)


        # contenedor lista de prendas
        self.encabezado = ('#1', '#2', '#3', '#4', '#5', '#6')
        self.tabla_clientes = ttk.Treeview(self.frm_lista_clientes, columns=self.encabezado, show='headings', height=10)
        self.tabla_clientes.pack(side='bottom', fill='both', padx=10, pady=10)

        self.tabla_clientes.column('#1', width=70, minwidth=70, stretch=False)
        self.tabla_clientes.column('#2', width=250, minwidth=250, stretch=False)
        self.tabla_clientes.column('#3', width=200, minwidth=200, stretch=False)
        self.tabla_clientes.column('#4', width=100, minwidth=100, stretch=False)
        self.tabla_clientes.column('#5', width=200, minwidth=200, stretch=False)
        self.tabla_clientes.column('#6', width=100, minwidth=100, stretch=False)

        self.tabla_clientes.heading('#1', text='CÓDIGO')
        self.tabla_clientes.heading('#2', text='NOMBRES DEL CLIENTE')
        self.tabla_clientes.heading('#3', text='DIRECCIÓN.')
        self.tabla_clientes.heading('#4', text='TELÉFONO')
        self.tabla_clientes.heading('#5', text='CORREO ELECTRÓNICO')
        self.tabla_clientes.heading('#6', text='CÉDULA')

        self.obtener_clientes()

        # Contenedor para los botones
        self.button_container = tk.Frame(self)
        self.button_container.pack(side="top")

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

        self.buscar = tk.StringVar()

        # Tell the entry widget to watch this variable.
        self.txtBuscar["textvariable"] = self.buscar

        self.buscar.trace('w', self.buscar_cliente)

        self.focus()

        self.grab_set()

    # Funcion para obtener la lista de clientes
    def obtener_clientes(self):

        # Limpiar la tabla
        for i in self.tabla_clientes.get_children():
            self.tabla_clientes.delete(i)

        # Conexión a la base de datos Azul lavandería
        db = dbConnection()

        cnx = db.cnx

        if cnx.is_connected():

            print("Esperando para enviar datos")

            cursor = cnx.cursor()

            # Llama al proceso almacenado
            cursor.callproc('spClientesRegistrados')

            for result in cursor.stored_results():
                self.clientes_registrados = result.fetchall()
                print(self.clientes_registrados)

            i = 1

            for cliente in self.clientes_registrados:
                print(cliente)
                i += 1
                self.tabla_clientes.insert("", 'end', iid=i,
                                           values=cliente)

            # Ejecutar el proceso almacenadoe
            cnx.commit()

            print(cursor.lastrowid)

            cursor.close()
            cnx.close()

        else:
            print("Connection failure")

    def buscar_cliente(self, *args):

        # Conexión a la base de datos Azul lavandería
        db = dbConnection()

        cnx = db.cnx

        texto_busqueda = self.buscar.get()

        if texto_busqueda == '':
            self.obtener_clientes()
        else:
            self.clientes_registrados = []

            # Limpiar la tabla
            for i in self.tabla_clientes.get_children():
                self.tabla_clientes.delete(i)

            if cnx.is_connected():

                print("Esperando para enviar datos")

                cursor = cnx.cursor()

                # Llama al proceso almacenado
                # To pass the input Arguments create a list and pass it
                buscador = [self.buscar.get(), ]
                cursor.callproc('spBuscarCliente', buscador)

                for result in cursor.stored_results():
                    self.clientes_registrados = result.fetchall()
                    print(self.clientes_registrados)
                i = 0
                for cliente in self.clientes_registrados:
                    print(cliente)
                    i += 1
                    self.tabla_clientes.insert("", 'end', iid=i,
                                               values=cliente)

                # Ejecutar el proceso almacenadoe
                cnx.commit()

                cursor.close()
                cnx.close()

            else:
                print("Connection failure")



