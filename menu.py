import tkinter as tk
from tkinter.messagebox import askyesno

from Cliente.FrmActualizarCliente import ActualizarCliente
from Cliente.FrmListadoClientes import ListadoClientes
from Cliente.FrmRegistrarCliente import RegistrarCliente
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
from time import strftime
from datetime import date, datetime

from Gastos.FrmRegistroGastos import FrmRegistroGastos
from Model.Usuario import Usuario
from OrdenTrabajo.FrmActualizarOrden import ActualizarOrden
from OrdenTrabajo.FrmOrdenesGeneradas import ListaOrdenes
from OrdenTrabajo.FrmNuevaOrden import NuevaOrden
from Producto.FrmInventarioProductos import FrmInventarioProductos
from RegistroDiario.FrmRegistroPagos import FrmRegistroPagos
from Ropa.FrmInventarioRopa import FrmInventarioPrendas
from TipoPrenda.FrmCatalogoPrendas import FrmCatalogoPrendas
from dbConnection import dbConnection


class MenuPrincipal(tk.Toplevel):

    def __init__(self, datos_usuario):

        super().__init__()

        self.datos_usuario = datos_usuario

        # Conexión a la base de datos Azul lavandería
        self.db = dbConnection()
        self.cnx = self.db.cnx

        self.lblTitulo = ttk.Label(self, text='Azul Lavandería', font=('Courier', 20), foreground='blue')
        self.lblTitulo.pack(side='top', padx=20, pady=5)

        # Contenedor mensaje de bienvenida y reloj
        self.contenedor_mensaje = tk.Frame(self)
        self.contenedor_mensaje.pack(side='top', fill='both')

        # Generar el mensaje de bienvenida
        self.msg_bienvenida = 'Bienvenid@: ' + self.datos_usuario.nombres + ' ' + self.datos_usuario.apellidos
        print(self.msg_bienvenida)

        self.lblBienvenida = ttk.Label(self.contenedor_mensaje, text=self.msg_bienvenida, font=('Courier', 12),foreground='green')
        self.lblBienvenida.pack(side='left', anchor='nw', padx=15, pady=5)

        self.label_reloj = ttk.Label(self.contenedor_mensaje, text='', font=('Courier', 12), foreground='gray')
        self.label_reloj.pack(side='right', padx=10, pady=0)

        # Pregunta de bienvenida
        self.lblQuestion = ttk.Label(self, text='Seleccione una opción: ', font=('Courier', 15), foreground='gray')
        self.lblQuestion.pack(side='top', anchor='nw', padx=15, pady=5)

        self.config(width=720, height=620)
        self.title("Menú principal")

        # Contenedores para cada opción
        self.main_container = tk.Frame(self)
        self.main_container.pack(side="top")

        self.container = tk.Frame(self.main_container)
        self.container.pack(side="left")

        self.container2 = tk.Frame(self.main_container)
        self.container2.pack(side="left")

        self.container3 = tk.Frame(self.main_container)
        self.container3.pack(side="left")

        self.container4 = tk.Frame(self.main_container)
        self.container4.pack(side="left")

        #Barra de menú
        self.menuBar =  tk.Menu(self)

        # Menú clientes
        self.menu_clientes = tk.Menu(self.menuBar, tearoff=False)

        # Opción para actualizar datos del cliente
        self.menu_clientes.add_command(
            label="Actualizar datos cliente",
            accelerator="Ctrl+A",
            command=self.actualizar_cliente
        )

        # Opción para ver clientes registrados
        self.menu_clientes.add_command(
            label="Clientes registrados",
            accelerator="Ctrl+L",
            command=self.clientes_registrados
        )

        # Opción para ingresar un nuevo cliente
        self.menu_clientes.add_command(
            label="Ingresar nuevo cliente",
            accelerator="Ctrl+N",
            command=self.nuevo_cliente
        )
        # Opción para generar nueva orden
        self.menu_clientes.add_command(
            label="Ordenes por cliente",
            accelerator="Ctrl+T"
        )

        # Menú de ordenes de trabajo
        self.menu_ordenes = tk.Menu(self.menuBar, tearoff=False)

        # Opción para buscar un cliente
        self.menu_ordenes.add_command(
            label="Nueva orden de trabajo",
            accelerator="Ctrl+O",
            command=self.generar_orden
        )

        # Opción para buscar un cliente
        self.menu_ordenes.add_command(
            label="Ordenes de trabajo generadas",
            accelerator="Ctrl+O",
            command=self.ordenes_generadas
        )

        # Opción para registrar una entrega
        self.menu_ordenes.add_command(
            label="Registrar entrega",
            accelerator="Ctrl+E",
            command=self.registrar_entrega
        )
        # Menú de gastos
        self.menu_gastos = tk.Menu(self.menuBar, tearoff=False)

        # Opción para registrar nuevo gasto
        self.menu_gastos.add_command(
            label="Control de gastos",
            accelerator="Ctrl+L",
            command=self.control_gastos
        )

        # Menú de reportes
        self.menu_reportes = tk.Menu(self.menuBar, tearoff=False)

        # Opción para generar el reporte de ventas
        self.menu_reportes.add_command(
            label="Reporte de cierre caja",
            accelerator="Ctrl+X",
            command=self.abrir_reportes

        )

        # Opción para visualizar el registro de conexion a cajas
        self.menu_reportes.add_command(
            label="Historial usuarios conectados",
            accelerator="Ctrl+X",
            command=self.abrir_historial

        )

        # Menú de reportes
        self.menu_inventario = tk.Menu(self.menuBar, tearoff=False)

        # Opción para agregar una prenda a inventario
        self.menu_inventario.add_command(
            label="Inventario de ropa",
            accelerator="Ctrl+I",
            command=self.inventario_ropa
        )

        # Opción para buscar un item
        self.menu_inventario.add_command(
            label="Inventario de productos",
            accelerator="Ctrl+M",
            command=self.inventario_productos
        )

        # Opción para buscar un item
        self.menu_inventario.add_command(
            label="Catálogo de prendas",
            accelerator="Ctrl+C",
            command=self.abrir_catalogo
        )

        self.menuBar.add_cascade(menu=self.menu_clientes, label="Clientes")
        self.menuBar.add_cascade(menu=self.menu_ordenes, label="Ordenes de trabajo")
        self.menuBar.add_cascade(menu=self.menu_reportes, label="Caja")
        self.menuBar.add_cascade(menu=self.menu_gastos, label="Gastos")
        self.menuBar.add_cascade(menu=self.menu_inventario, label="Inventario")

        self.config(menu=self.menuBar)

        # Create an object of tkinter ImageTk
        self.readImg = Image.open("Img/ordenTrabajo.png")
        self.newImg = self.readImg.resize((120, 120))
        self.img = ImageTk.PhotoImage(self.newImg)

        self.button_order = ttk.Button(
            self.container,
            text="GENERAR ORDEN DE TRABAJO",
            command=self.generar_orden,
            width=28,
            image=self.img,
            compound='top'
        )
        self.button_order.pack(side='bottom', padx=10, pady=5, ipadx=5, ipady=5)

        # Botón para generar ordenes de pago

        # Create an object of tkinter ImageTk
        self.readImg2 = Image.open("Img/registroEntrega.png")
        self.newImg2 = self.readImg2.resize((120, 120))
        self.img2 = ImageTk.PhotoImage(self.newImg2)

        self.button_entrega = ttk.Button(
            self.container2,
            text="REGISTRAR ENTREGA",
            command=self.registrar_entrega,
            width=28,
            image=self.img2,
            compound='top'
        )
        self.button_entrega.pack(side='left', padx=10, pady=5, ipadx=5, ipady=5)

        # Botón para ver inventario

        # Create an object of tkinter ImageTk
        self.readImg3 = Image.open("Img/inventario.png")
        self.newImg3 = self.readImg3.resize((120, 120))
        self.img3 = ImageTk.PhotoImage(self.newImg3)

        self.button_viewInventario = ttk.Button(
            self.container3,
            text="INVENTARIO PRODUCTOS",
            command=self.inventario_productos,
            width=28,
            image=self.img3,
            compound='top'
        )
        self.button_viewInventario.pack(side='bottom', padx=10, pady=5, ipadx=5, ipady=5)

        # Botón para cerrar sesión

        # Create an object of tkinter ImageTk
        self.readImg4 = Image.open("Img/cancel.png")
        self.newImg4 = self.readImg4.resize((120, 120))
        self.img4 = ImageTk.PhotoImage(self.newImg4)

        self.button_salir = ttk.Button(
            self.container4,
            text="SALIR",
            command=self.cerrar_sesion,
            width=28,
            image=self.img4,
            compound='top'
        )
        self.button_salir.pack(side='bottom', padx=10, pady=5, ipady=5, ipadx=5)

        # Créditos Ticscode
        self.lblQuestion = ttk.Label(self, text='Desarrollado por: TicsCode Ecuador | www.ticscode.com', font=('Arial', 8), foreground='gray')
        self.lblQuestion.pack(side='top', anchor='center', padx=15, pady=20)

        self.time()

        self.focus()
        self.grab_set()

    def nuevo_cliente(self):
        RegistrarCliente(self.datos_usuario)

    def clientes_registrados(self):
        lista_clientes = ListadoClientes(self.datos_usuario)
        lista_clientes.maxsize(width=950, height=600)

    def actualizar_cliente(self):
        ActualizarCliente(self.datos_usuario)

    def generar_orden(self):
        frm_orden=NuevaOrden(self.datos_usuario)
        frm_orden.wm_maxsize(width=720, height=710)

    def ordenes_generadas(self):
        frm_lista_ordenes=ListaOrdenes(self.datos_usuario)
        frm_lista_ordenes.wm_maxsize(width=950, height=770)

    def registrar_entrega(self):
        frm_entrega=ActualizarOrden(self.datos_usuario)
        frm_entrega.wm_maxsize(width=700, height=770)

    def inventario_productos(self):
        frm_inventario = FrmInventarioProductos(self.datos_usuario)

    def cerrar_sesion(self):

        # Conexión a la base de datos Azul lavandería
        db = dbConnection()
        cnx = db.cnx

        answer = askyesno(title='Cerrar sesión',
                          message='¿Desea cerrar la caja?')
        if answer:
            if cnx.is_connected():
                cursor = cnx.cursor()

                # Obtener el total de las ordenes generadas en el día
                args = [datetime.now()]
                cursor.callproc('spTotalizarVentas', args)

                response = []

                for result in cursor.stored_results():
                    response = result.fetchall()
                    print(response)

                cnx.commit()

                total_ventas = response[0][0]

                print('TOTAL GENERADO: ' + str(total_ventas))

                # Obtener el total de las importes ingresados en el día
                cursor.callproc('spTotalizarImportes', args)

                response = []

                for result in cursor.stored_results():
                    response = result.fetchall()
                    print(response)

                total_importes = response[0][0]

                print('TOTAL IMPORTES: ' + str(total_importes))

                # Obtener el total de los gastos ingresados en el día
                cursor.callproc('spTotalizarGastos', args)

                response = []

                for result in cursor.stored_results():
                    response = result.fetchall()
                    print(response)

                total_gastos = response[0][0]

                print('TOTAL GASTOS: ' + str(total_gastos))

                # Registrar el cierre de sesión
                datos_cierre = [self.datos_usuario.id_caja, datetime.now(), total_ventas,
                                total_importes, total_gastos]

                cursor.callproc('spRegistrarCierreCaja', datos_cierre)

                cnx.commit()

                if cursor.rowcount != 0:
                    print('.....REGISTRO DE CIERRE EXITOSO......!!!')

            else:
                print('No se pudo conectar a la BD')

            self.master.deiconify()
            self.destroy()

    def time(self):
        string = strftime('%H:%M:%S %p')
        self.label_reloj.config(text=string)
        self.label_reloj.after(1000, self.time)

    def abrir_reportes(self):
        frm_registro_pagos = FrmRegistroPagos(self.datos_usuario)
        frm_registro_pagos.wm_maxsize(width=1230, height=770)

    def control_gastos(self):
        frmRegistroGastos = FrmRegistroGastos(self.datos_usuario)

    def abrir_historial(self):
        pass

    def inventario_ropa(self):
        frm_inventario_ropa = FrmInventarioPrendas(self.datos_usuario)

    def abrir_catalogo(self):
        frm_catalogo_prendas = FrmCatalogoPrendas(self.datos_usuario)