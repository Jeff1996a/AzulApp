import datetime
import tkinter as tk
import win32print
import win32ui
import win32api
import os
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
from tkcalendar import *
from datetime import date
from fpdf import FPDF


from dbConnection import dbConnection


class NuevaOrden(tk.Toplevel):

    def __init__(self, datos_usuario):

        super().__init__()

        self.datos_usuario = datos_usuario

        print('El id del usuario ' + str(self.datos_usuario.id))

        # Variable asociadas a cada campo de la prenda
        self.tipo_prenda=tk.StringVar()
        self.tipo_servicio=tk.StringVar()
        self.observacion=tk.StringVar()
        self.cantidad = tk.IntVar()

        # Tipo de pago
        self.tipo_pago = tk.StringVar()

        # Contador de prendas
        self.contador_prendas = 0

        # Variable para llevar el pago general de la orden
        self.total_pagar = 0.0

        self.lblTitulo = ttk.Label(self, text='Azul Lavandería', font=('Courier', 20), foreground='blue')
        self.lblTitulo.pack(side='top', padx=10, pady=0)

        # Pregunta de bienvenida
        self.lblNuevaOrden = ttk.Label(self, text='Nueva orden de trabajo ', font=('Courier', 15),
                                                foreground='purple')
        self.lblNuevaOrden.pack(side='top', anchor='center', padx=10, pady=0)

        # Fila 1
        self.frame1 = tk.Frame(self)
        self.frame1.pack(side='top', fill='both', padx=10, pady=4)

        # Frame cliente
        self.cliente_container = tk.LabelFrame(self.frame1,text='DATOS CLIENTE', font=("Courier", 12), foreground='green')
        self.cliente_container.pack(side='left', fill='both', ipadx=5, ipady=4)

        # Contenedor para el id el cliente
        self.id_container = tk.Frame(self.cliente_container)
        self.id_container.pack(side="top", fill='both')
        self.id_container.pack_forget()

        # Text nombres del cliente
        self.txtId = ttk.Entry(self.id_container, width=10)
        self.txtId.pack(side='left', padx=0, pady=2, ipadx=2, ipady=2)
        self.txtId.config(state='disabled')

        # Contenedor para la cédula del cliente
        self.cedula_container = tk.Frame(self.cliente_container)
        self.cedula_container.pack(side="top", fill='both')

        # Label cédula del cliente
        self.lblcedula = ttk.Label(self.cedula_container, text='CÉDULA O RUC:', font=("Courier", 10), width=20)
        self.lblcedula.pack(side='left', anchor='nw', padx=0, pady=2, ipadx=2, ipady=0)

        # Text cédula del cliente
        self.txtCedula = ttk.Entry(self.cedula_container, width=20)
        self.txtCedula.pack(side='left', padx=0, pady=2, ipadx=2, ipady=0)
        self.txtCedula.focus_set()

        self.txtCedula.bind('<FocusOut>', self.buscar_cliente)

        # Contenedor para los nombres del cliente
        self.nombres_container = tk.Frame(self.cliente_container)
        self.nombres_container.pack(side="top", fill='both')

        # Label nombres del cliente
        self.lblname = ttk.Label(self.nombres_container, text='APELLIDOS Y NOMBRES:', font=("Courier", 10), width=20)
        self.lblname.pack(side='left', anchor='nw', padx=0, pady=2, ipadx=2, ipady=0)

        # Text nombres del cliente
        self.txtnombre = ttk.Entry(self.nombres_container, width=45)
        self.txtnombre.pack(side='left', padx=0, pady=2, ipadx=2, ipady=0)

        # Contenedor para la dirección del cliente
        self.direccion_container = tk.Frame(self.cliente_container)
        self.direccion_container.pack(side="top", fill='both')

        # Label direccion del cliente
        self.lbldireccion = ttk.Label(self.direccion_container, text='DIRECCIÓN:', font=("Courier", 10), width=20)
        self.lbldireccion.pack(side='left', anchor='nw', padx=0, pady=2, ipadx=2, ipady=0)

        # Text direccion del cliente
        self.txtDireccion = ttk.Entry(self.direccion_container, width=40)
        self.txtDireccion.pack(side='left', padx=0, pady=2, ipadx=2, ipady=0)

        # Contenedor teléfono del cliente
        self.telefono_container = tk.Frame(self.cliente_container)
        self.telefono_container.pack(side="top", fill='both')

        # Label telefono del cliente
        self.lblTelefono = ttk.Label(self.telefono_container, text='TELÉFONO:', font=("Courier", 10), width=20)
        self.lblTelefono.pack(side='left', anchor='nw', padx=0, pady=2, ipadx=2, ipady=0)

        # Text telefono del cliente
        self.txtTelefono = ttk.Entry(self.telefono_container, width=20)
        self.txtTelefono.pack(side='left', padx=0, pady=2, ipadx=2, ipady=0)

        # Contenedor email del cliente
        self.email_container = tk.Frame(self.cliente_container)
        self.email_container.pack(side="top", fill='both')

        # Label telefono del cliente
        self.lblEmail = ttk.Label(self.email_container, text='CORREO ELECTRÓNICO:', font=("Courier", 10), width=20)
        self.lblEmail.pack(side='left', anchor='nw', padx=0, pady=2, ipadx=2, ipady=0)

        # Text telefono del cliente
        self.txtEmail = ttk.Entry(self.email_container, width=40)
        self.txtEmail.pack(side='left', padx=0, pady=2, ipadx=2, ipady=0)

        #*****************************************************************************************************
        # Lista de metodos de pago
        self.metodos = []

        self.obtener_metodos_pago()

        self.descripcion_metodos = []

        for metodo in self.metodos:
            self.descripcion_metodos.append(metodo[0])

        # Contenedor detalles orden
        self.orden_container = tk.LabelFrame(self.frame1, text='DETALLES DEL PEDIDO', font=("Courier", 12), foreground='green')
        self.orden_container.pack(side='right', fill='both')

        # Número de orden container
        self.num_order_container = tk.Frame(self.orden_container)
        self.num_order_container.pack(side='top', fill='both', ipadx=2, ipady=0, padx=0, pady=2)

        # Label número de orden
        self.lbl_num_order = ttk.Label(self.num_order_container, text='ORDEN N°:', font=("Courier", 10), width=15, foreground='purple')
        self.lbl_num_order.pack(side='left', anchor='nw', padx=0, pady=2, ipadx=2, ipady=0)

        # Text número de orden
        self.txt_num_order = ttk.Entry(self.num_order_container, width=15)
        self.txt_num_order.pack(side='left', padx=0, pady=2, ipadx=2, ipady=0)
        self.txt_num_order.config(state='readonly')

        # Contenedor método de pago
        self.contenedor_metodo = ttk.Frame(self.orden_container)
        self.contenedor_metodo.pack(side='top',fill='both', ipadx=3, ipady=0, padx=0, pady=0)

        # Label tipo de servicio
        self.label_metodo= ttk.Label(self.contenedor_metodo, text='MÉTODO PAGO:', font=("Courier", 10), width=15)
        self.label_metodo.pack(side='left', padx=0, pady=2,  ipadx=2, ipady=0)

        # Combo método de pago
        self.combo_metodo = ttk.Combobox(self.contenedor_metodo, width=11,
                                            values=self.descripcion_metodos, font=("Courier", 8), textvariable=self.tipo_pago)
        self.combo_metodo.pack(side='left', padx=0, pady=2,  ipadx=0, ipady=0)

        # Fecha de entrada
        self.fecha_orden_container = tk.Frame(self.orden_container)
        self.fecha_orden_container.pack(side='top', fill='both', ipadx=2, ipady=0, padx=0, pady=2)

        # Label fecha de entrada
        self.lbl_fecha_order = ttk.Label(self.fecha_orden_container, text='FECHA PEDIDO:', font=("Courier", 10), width=15)
        self.lbl_fecha_order.pack(side='left', anchor='nw', padx=0, pady=2, ipadx=2, ipady=0)

        # Text fecha de entrada
        self.txt_fecha_order = ttk.Entry(self.fecha_orden_container, width=15)
        self.txt_fecha_order.pack(side='left', padx=0, pady=2, ipadx=2, ipady=0)
        self.txt_fecha_order.config(state='readonly')

        # Fecha de entrega
        self.fecha_entrega_container = tk.Frame(self.orden_container)
        self.fecha_entrega_container.pack(side='top', fill='both', ipadx=2, ipady=0, padx=0, pady=2)

        # Label fecha de entrada
        self.lbl_fecha_entrega = ttk.Label(self.fecha_entrega_container, text='FECHA ENTREGA:', font=("Courier", 10),
                                         width=15)
        self.lbl_fecha_entrega.pack(side='left', anchor='nw', padx=0, pady=2, ipadx=2, ipady=0)

        # Text fecha de entrada
        self.txt_fecha_entrega = ttk.Entry(self.fecha_entrega_container, width=15)
        self.txt_fecha_entrega.pack(side='left', padx=0, pady=2, ipadx=2, ipady=0)
        self.txt_fecha_entrega.insert(0, "yyyy/dd/mm")

        # Calendario de fecha entrada
        self.date_frame = tk.Frame(self.orden_container)

        self.cal = Calendar(self.date_frame, selectmode='day', date_pattern='y-mm-dd')

        self.submit_date = ttk.Button(self.date_frame, text='INGRESAR', width=15, command=self.grab_date)
        self.txt_fecha_entrega.bind('<1>', self.pick_date)


        # ******************************************************************************************************
        # Contenedor tabla prendas
        self.contenedor_tabla=tk.LabelFrame(self, text='AGREGAR PRENDAS/ACCESORIOS' , font=("Courier", 12), foreground='green')
        self.contenedor_tabla.pack(side='top', fill='both', padx=10, pady=0)

        # Contenedor del botón para agregar mas prendas
        self.contenedor_btn_agregar = tk.Frame(self.contenedor_tabla)
        self.contenedor_btn_agregar.pack(side='top', fill='both')

        # ***********************************************************************************************************
        self.contenedor_frm_agregar_item=tk.Frame(self.contenedor_tabla)
        self.contenedor_frm_agregar_item.pack(side='top', fill='both', padx=10, pady=0)

        # Lista de prendas de vestir
        self.prendas = []

        # Lista de servicios
        self.servicios = []

        # Llamar a la función para obtener servicios
        self.obtener_servicios()

        self.descripcion_prenda = []
        self.descripcion_servicios = []

        for servicio in self.servicios:
            self.descripcion_servicios.append(servicio[1])

        # Label tipo de servicio
        self.label_tipo_serv = ttk.Label(self.contenedor_frm_agregar_item, text='Tipo de servicio:')
        self.label_tipo_serv.grid(sticky='nw', row=0, column=0, padx=5, pady=3)

        # Text tipo servicio
        self.combo_tipo_serv = ttk.Combobox(self.contenedor_frm_agregar_item, width=20,
                                                values=self.descripcion_servicios)
        self.combo_tipo_serv.grid(sticky='nw', row=0, column=1, padx=5, pady=3)
        self.combo_tipo_serv.bind('<<ComboboxSelected>>', self.validar_servicio)

        self.label_tipo_prenda = ttk.Label(self.contenedor_frm_agregar_item, text='Prenda / Producto:')
        self.label_tipo_prenda.grid(row=1, column=0, padx=5, pady=3)

        # Text saldo cliente
        self.combo_tipo_prenda = ttk.Combobox(self.contenedor_frm_agregar_item, width=40, values=self.descripcion_prenda,
                                              textvariable=self.tipo_prenda)
        self.combo_tipo_prenda.grid(row=1,column=1, padx=5, pady=0)
        self.combo_tipo_prenda.bind('<KeyRelease>', self.completar_combobox)

        # Create an object of tkinter ImageTk
        self.addImg = Image.open("Img/add.png")
        self.newAddImg = self.addImg.resize((15, 15))
        self.add = ImageTk.PhotoImage(self.newAddImg)

        # Label cantidad
        self.label_cantidad = ttk.Label(self.contenedor_frm_agregar_item, text='Cantidad:')
        self.label_cantidad.grid(sticky='nw', row=2, column=0, padx=5, pady=3)

        # Text saldo cliente
        self.txt_cantidad_prendas = ttk.Entry(self.contenedor_frm_agregar_item, width=10, textvariable=self.cantidad)
        self.txt_cantidad_prendas.grid(sticky='nw',row=2, column=1, padx=5, pady=3)

        # Label cantidad
        self.label_obs = ttk.Label(self.contenedor_frm_agregar_item, width=12, text='Observación:')
        self.label_obs.grid(sticky='nw', row=2, column=2, padx=0, pady=3)

        # Observaciones
        self.txt_observacion = ttk.Entry(self.contenedor_frm_agregar_item, width=40)
        self.txt_observacion.grid(sticky='nw', row=2, column=3, padx=0, pady=3)

        self.txt_observacion['textvariable'] = self.observacion

        self.cantidad.set(0)

        # Botón para agregar prendas
        self.btn_agregar_prenda = ttk.Button(
            self.contenedor_frm_agregar_item,
            text="AGREGAR",
            image=self.add,
            compound='right',
            command=self.agregar_prenda
        )
        self.btn_agregar_prenda.grid(row=0, column=2, padx=20, pady=0)

        #contenedor lista de prendas
        self.encabezado = ('#1', '#2', '#3', '#4', '#5', '#6')
        self.tabla_prendas = ttk.Treeview(self.contenedor_tabla,columns=self.encabezado, show='headings', height=4)
        self.tabla_prendas.pack(side='top', fill='both', padx=10, pady=10)

        self.context_menu = tk.Menu(self.tabla_prendas, tearoff=0)
        self.context_menu.add_command(label="Eliminar", command=self.eliminar_prenda)

        self.tabla_prendas.bind("<Button-3>", self.popup)

        self.tabla_prendas.column('#1',width=200, minwidth=200, stretch=False)
        self.tabla_prendas.column('#2',width=120, minwidth=120, stretch=False)
        self.tabla_prendas.column('#3',width=70, minwidth=70, stretch=False, anchor='center')
        self.tabla_prendas.column('#4',width=70, minwidth=70, stretch=False, anchor='center')
        self.tabla_prendas.column('#5',width=70, minwidth=70, stretch=False, anchor='center')
        self.tabla_prendas.column('#6',width=170, minwidth=170, stretch=False, anchor='center')

        self.tabla_prendas.heading('#1', text='PRENDA/ACCESORIO', anchor='center')
        self.tabla_prendas.heading('#2', text='TIPO DE SERVICIO', anchor='center')
        self.tabla_prendas.heading('#3', text='CANT.', anchor='center')
        self.tabla_prendas.heading('#4', text='PRECIO ($)', anchor='center')
        self.tabla_prendas.heading('#5', text='TOTAL ($)', anchor='center')
        self.tabla_prendas.heading('#6', text='OBSERVACIONES', anchor='center')

        # Contenedor para los abonos, saldos y totales
        self.total = tk.DoubleVar()
        self.saldo = tk.DoubleVar()
        self.abono = tk.DoubleVar()

        self.contenedor_saldos = tk.LabelFrame(self, text='ABONOS Y SALDOS' , font=("Courier", 12), foreground='green')
        self.contenedor_saldos.pack(side='top', anchor='center' , fill='both', padx=10, pady=0, ipadx=10, ipady=3)

        # Abono cliente
        self.abono_container = tk.Frame(self.contenedor_saldos)
        self.abono_container.pack(side='left', anchor='w', ipadx=2, ipady=0, padx=0, pady=2)

        # Label abono cliente
        self.lbl_abono = ttk.Label(self.abono_container, text='IMPORTE ($):', font=("Courier", 12),
                                   foreground='purple')
        self.lbl_abono.pack(side='left', padx=0, pady=2, ipadx=2, ipady=2)

        # Text abono cliente
        self.txt_abono = ttk.Entry(self.abono_container, width=10, font=("Arial", 13))
        self.txt_abono.pack(side='left', padx=0, pady=2, ipadx=2, ipady=2, )

        self.txt_abono['textvariable'] = self.abono
        self.abono.set(0.0)

        self.txt_abono.bind('<FocusOut>', self.calcular_saldo)

        # Saldo cliente
        self.saldo_container = tk.Frame(self.contenedor_saldos)
        self.saldo_container.pack(side='left', anchor='center', ipadx=2, ipady=0, padx=0, pady=2)

        # Label saldo cliente
        self.lbl_saldo = ttk.Label(self.saldo_container, text='SALDO ($):', font=("Courier", 12),
                                    foreground='blue')
        self.lbl_saldo.pack(side='left',  padx=0, pady=2, ipadx=2, ipady=2)

        # Text saldo cliente
        self.txt_saldo = ttk.Entry(self.saldo_container, width=10, font=("Arial", 13))
        self.txt_saldo.pack(side='left', padx=0, pady=2, ipadx=2, ipady=2)
        self.txt_saldo.config(state='readonly')

        self.txt_saldo['textvariable'] = self.saldo
        self.saldo.set(0.0)

        # Total a pagar contenedor
        self.total_container = tk.Frame(self.contenedor_saldos)
        self.total_container.pack(side='right', anchor='e', ipadx=2, ipady=0, padx=0, pady=2)

        # Label saldo cliente
        self.lbl_total = ttk.Label(self.total_container, text='TOTAL A PAGAR ($):', font=("Courier", 12), foreground='red')
        self.lbl_total.pack(side='left', padx=0, pady=2, ipadx=2, ipady=2)

        # Text saldo cliente
        self.txt_total = ttk.Entry(self.total_container, width=10, font=("Arial", 13))
        self.txt_total.pack(side='left', padx=0, pady=2, ipadx=2, ipady=2)
        self.txt_total.config(state='readonly')

        self.txt_total['textvariable'] = self.total

        self.total.set(0.0)

        # ************************************************************************************************************

        # Contenedor observaciones generales
        self.contenedor_observaciones = tk.LabelFrame(self, text='OBSERVACIONES GENERALES', font=("Courier", 12), foreground='green')
        self.contenedor_observaciones.pack(side='top', fill='both', padx=10, pady=0, ipadx=5, ipady=0)

        # Text observaciones generales
        self.txt_observaciones = ttk.Entry(self.contenedor_observaciones, width=120)
        self.txt_observaciones.pack(side='left', anchor='center', padx=0, pady=5, ipadx=2, ipady=2)

        # Contenedor para los botones
        self.button_container = tk.Frame(self)
        self.button_container.pack(side="top")

        # Create an object of tkinter ImageTk
        self.saveImg = Image.open("Img/save.png")
        self.newSaveImg = self.saveImg.resize((15, 15))
        self.save = ImageTk.PhotoImage(self.newSaveImg)

        # Botón para guardar los datos
        self.guardar_button = ttk.Button(
            self.button_container,
            text="GENERAR ORDEN",
            command=self.generar_orden,
            image=self.save,
            compound='right',
        )
        self.guardar_button.pack(side='left', anchor='center', padx=10, pady=5, ipadx=5, ipady=3)

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
        self.cancelar_registro.pack(side='right', anchor='center', padx=10, pady=5, ipadx=5, ipady=3)

        # Variables datos del cliente
        self.idCliente = tk.IntVar()
        self.cedula = tk.StringVar()
        self.nombres = tk.StringVar()
        self.direccion = tk.StringVar()
        self.telefono = tk.StringVar()
        self.email = tk.StringVar()

        self.txtId['textvariable'] = self.idCliente
        self.txtCedula['textvariable'] = self.cedula
        self.txtnombre['textvariable'] = self.nombres
        self.txtDireccion['textvariable'] = self.direccion
        self.txtTelefono['textvariable'] = self.telefono
        self.txtEmail['textvariable'] = self.email

        # Variables del pedido
        self.num_orden = tk.StringVar()
        self.fecha_pedido = tk.StringVar()
        self.fecha_entrega = tk.StringVar()
        self.observacion_general = tk.StringVar()

        self.txt_num_order['textvariable'] = self.num_orden
        self.txt_fecha_order['textvariable'] = self.fecha_pedido
        self.txt_fecha_entrega['textvariable'] = self.fecha_entrega
        self.txt_observaciones['textvariable'] = self.observacion_general

        self.fecha_pedido.set(date.today().strftime("%Y-%m-%d"))
        self.fecha_entrega.set('yyyy-mm-dd')

        self.nombres.trace('w', self.upper_nombres)
        self.direccion.trace('w', self.upper_direccion)

        self.obtener_num_orden()

        # Prendas agregadas
        self.prendas_agregadas = []

        self.focus()

        self.grab_set()


    # Función para buscar cliente
    def buscar_cliente(self,event):

        self.clientes_registrados = []

        # Conexión a la base de datos Azul lavandería
        db = dbConnection()

        cnx = db.cnx

        if cnx.is_connected():

            print("Esperando para enviar datos")

            cursor = cnx.cursor()

            # Llama al proceso almacenado
            # To pass the input Arguments create a list and pass it
            buscador = [self.cedula.get()]
            cursor.callproc('spBuscarCliente', buscador)

            for result in cursor.stored_results():
                self.clientes_registrados = result.fetchall()
                print(self.clientes_registrados)

            i = 1

            self.cliente_encontrado = []

            for cliente in self.clientes_registrados:
                self.cliente_encontrado = cliente

            print(self.cliente_encontrado)

            self.idCliente.set(self.cliente_encontrado[0])
            self.nombres.set(self.cliente_encontrado[1])
            self.direccion.set(self.cliente_encontrado[2])
            self.telefono.set(self.cliente_encontrado[3])
            self.email.set(self.cliente_encontrado[4])
            self.cedula.set(self.cliente_encontrado[5])

            # Ejecutar el proceso almacenadoe
            cnx.commit()

            cursor.close()
            cnx.close()

        else:
            print("Connection failure")

    # Función para obtener la lista de prendas
    def obtener_prendas(self):
        # Conexión a la base de datos Azul lavandería
        db = dbConnection()

        cnx = db.cnx

        lista_prendas = []

        if cnx.is_connected():

            print("Esperando para obtener prendas")

            cursor = cnx.cursor()

            # Llama al proceso almacenado
            cursor.callproc('spObtenerPrendas')

            for result in cursor.stored_results():
                lista_prendas = result.fetchall()
                print(lista_prendas)

            i = 1

            self.prendas = []

            for prenda in lista_prendas:
                self.prendas.append(prenda)
            print(self.prendas)

            # Ejecutar el proceso almacenadoe
            cnx.commit()

            cursor.close()
            cnx.close()

        else:
            print("Connection failure")

    # Función para obtener el tipo de servicio
    def obtener_servicios(self):

        # Conexión a la base de datos Azul lavandería
        db = dbConnection()

        cnx = db.cnx

        lista_servicios = []

        if cnx.is_connected():

            print("Esperando para obtener prendas")

            cursor = cnx.cursor()

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
            cnx.commit()

            cursor.close()
            cnx.close()

        else:
            print("Connection failure")

    # Función para obtener los métodos de pago disponibles
    def obtener_metodos_pago(self):

        # Conexión a la base de datos Azul lavandería
        db = dbConnection()
        cnx = db.cnx

        lista_metodos = []

        if cnx.is_connected():

            print("....OBTENIENDO MÉTODOS DE PAGO.....")

            cursor = cnx.cursor()

            # Llama al proceso almacenado
            cursor.callproc('spObtenerMetodosPago')

            for result in cursor.stored_results():
                lista_metodos = result.fetchall()
                print(lista_metodos)

            self.metodos = []

            for metodo in lista_metodos:
                self.metodos.append(metodo)
            print(self.metodos)

            cursor.close()
            cnx.close()

        else:
            print("Connection failure")

    # Función para autocompletar combobox
    def completar_combobox(self, event):

        value = event.widget.get()
        print(value)

        data = []
        # get data from l
        if value == '':
            self.combo_tipo_prenda['values']=self.descripcion_prenda
        else:

            for item in self.descripcion_prenda:
                if value.lower() in item.lower():
                    data.append(item)

        self.combo_tipo_prenda['values'] = data

    # Agregar el tipo de prenda a la orden
    def agregar_prenda(self):

        # Conexión a la base de datos Azul lavandería
        db = dbConnection()
        cnx = db.cnx

        tipo_prenda = self.combo_tipo_prenda.get()
        tipo_servicio = self.combo_tipo_serv.get()
        observacion = self.txt_observacion.get()
        cantidad = self.cantidad.get()
        abono = self.txt_abono.get()

        precio = 0

        if tipo_prenda == '':
            messagebox.showerror(message='Por favor, seleccionar un tipo de prenda', title='Error de registro')
        elif tipo_servicio == '':
            messagebox.showerror(message='Por favor, seleccionar el tipo de servicio', title='Error de registro')
        elif cantidad == 0:
            messagebox.showerror(message='Por favor, Ingresar la cantidad de prendas', title='Error de registro')
        else:
            lista_prendas = []

            if cnx.is_connected():

                if tipo_servicio != 'PRODUCTO':

                    print(".....OBTENIENDO PRECIOS......")

                    cursor = cnx.cursor()

                    # Llama al proceso almacenado
                    nueva_prenda = [tipo_prenda, tipo_servicio]

                    cursor.callproc('spObtenerPrecioPrenda', nueva_prenda)

                    for result in cursor.stored_results():
                        lista_prendas = result.fetchall()
                        print(lista_prendas)

                    i = 1

                    if len(lista_prendas) == 0:
                        messagebox.showerror(message='No se encontró el item seleccionado', title='Error de registro')
                    else:
                        precio = float(lista_prendas[0][0])

                        print('Tipo de prenda seleccionado:' + tipo_prenda)
                        print('Tipo de servicio seleccionado:' + tipo_servicio)
                        print('Cantidad:' + str(cantidad))
                        print('Precio:' + str(precio))
                        print('Total:' + str(precio * float(cantidad)))

                        self.total_pagar += precio * float(cantidad)

                        self.total.set(round(self.total_pagar, 2))
                        saldo = self.total_pagar - float(abono)
                        self.saldo.set(round(saldo, 2))

                        self.contador_prendas += 1

                        prenda = (tipo_prenda, tipo_servicio, cantidad, round(precio, 2), round(precio * float(cantidad),2), observacion )

                        self.prendas_agregadas.append(prenda)

                        self.tabla_prendas.insert("", 'end', iid=self.contador_prendas,
                                                  values=(
                                                   tipo_prenda, tipo_servicio, cantidad, round(precio,2), round(precio * float(cantidad), 2), observacion))

                        self.combo_tipo_prenda.set('')
                        self.combo_tipo_serv.set('')
                        self.cantidad.set(0)
                        self.observacion.set('')

                    # Ejecutar el proceso almacenado
                    cnx.commit()

                    cursor.close()
                    cnx.close()
                else:
                    print(".....OBTENIENDO PRECIOS.....")

                    cursor = cnx.cursor()

                    # Llama al proceso almacenado
                    argumento = [tipo_prenda]

                    cursor.callproc('spObtenerProductoPorDescripcion', argumento)

                    for result in cursor.stored_results():
                        lista_prendas = result.fetchall()
                        print(lista_prendas)

                    i = 1

                    if len(lista_prendas) == 0:
                        messagebox.showerror(message='No se encontró el item seleccionado', title='Error de registro')
                    else:
                        id_producto = lista_prendas[0][0]
                        descripcion_producto = lista_prendas[0][1]
                        precio = float(lista_prendas[0][4])
                        cantidad_producto = float(lista_prendas[0][2])
                        stock = lista_prendas[0][3]
                        observacion_producto = lista_prendas[0][5]

                        if int(cantidad) > int(cantidad_producto):

                            msg = 'Existen solo ' + str(int(cantidad_producto)) + ' productos en el inventario'
                            messagebox.showerror(message=msg,
                                                 title='Error de registro')
                        else:

                            cantidad_restante = int(cantidad_producto) - int(cantidad)

                            print('Id producto: ' + str(id_producto))
                            print('Tipo de producto seleccionado:' + descripcion_producto)
                            print('Cantidad:' + str(cantidad))
                            print('Cantidad inventario: ' + str(cantidad_producto))
                            print('Cantidad restante: ' + str(cantidad_restante))
                            print('Precio:' + str(precio))
                            print('Total:' + str(precio * float(cantidad)))
                            print('Observacion:' + observacion_producto)

                            # Llama al proceso almacenado
                            argumento = [id_producto, descripcion_producto, cantidad_restante,
                                         stock, precio, observacion_producto]

                            cursor.callproc('spActualizarProducto', argumento)

                            # Ejecutar el proceso almacenado
                            cnx.commit()

                            self.total_pagar += precio * float(cantidad)

                            self.total.set(round(self.total_pagar, 2))
                            saldo = self.total_pagar - float(abono)
                            self.saldo.set(round(saldo, 2))

                            self.contador_prendas += 1

                            prenda = (
                                tipo_prenda, tipo_servicio, cantidad, round(precio, 2), round(precio * float(cantidad),2),
                                observacion)

                            self.prendas_agregadas.append(prenda)

                            self.tabla_prendas.insert("", 'end', iid=self.contador_prendas,
                                                      values=(
                                                          tipo_prenda, tipo_servicio, cantidad, round(precio, 2),
                                                          round(precio * float(cantidad), 2), observacion))

                            self.combo_tipo_prenda.set('')
                            self.combo_tipo_serv.set('')
                            self.cantidad.set(0)
                            self.observacion.set('')

                            cursor.close()
                            cnx.close()

                        cursor.close()
                        cnx.close()
            else:
                print("Connection failure")

    def pick_date(self, event):
        self.date_frame.pack(side='top')
        self.cal.pack(side='top')
        self.submit_date.pack(side='top')

    def grab_date(self):
        self.txt_fecha_entrega.delete(0, 'end')
        self.txt_fecha_entrega.insert(0, self.cal.get_date())
        self.date_frame.pack_forget()

    # Calcular saldo restante de la orden
    def calcular_saldo(self, event):

        total_pagar = self.total.get()
        abono = self.abono.get()
        
        if abono > total_pagar:
            messagebox.showerror(message='El abono no puede ser mayor al total de la venta', title='Error de ingreso')
            self.abono.set(0)
            self.txt_abono.focus()
        elif abono < 0:
            messagebox.showerror(message='El abono no puede ser negativo', title='Error de ingreso')
            self.abono.set(0)
            self.txt_abono.focus()
        else:
            saldo = total_pagar - abono
            self.saldo.set(round(saldo,2))

    # Función para generar la orden de trabajo
    def generar_orden(self):

        # Conexión a la base de datos Azul lavandería
        db = dbConnection()
        cnx = db.cnx

        id_orden = 0

        # Obtener datos del cliente
        print('***** DATOS DEL CLIENTE *****')
        id_cliente = self.idCliente.get()
        print('Id Cliente: ' + str(id_cliente))

        # Registrar nuevo cliente si no existe
        if id_cliente == 0 and self.cedula.get() != '':

            if cnx.is_connected():

                print(".......CONSULTANDO CLIENTE......")

                cursor = cnx.cursor()

                # Llama al proceso almacenado
                # To pass the input Arguments create a list and pass it
                buscador = [self.cedula.get(), ]
                cursor.callproc('spBuscarCliente', buscador)

                datos_cliente=[]

                for result in cursor.stored_results():
                    datos_cliente = result.fetchall()
                    print(datos_cliente)

                if len(datos_cliente) == 0:
                    print('....CLIENTE NO REGISTRADO......')

                    print("....REGISTRANDO NUEVO USUARIO.....")

                    # To pass the input Arguments create a client
                    client_data = [self.nombres.get(), self.direccion.get(), self.telefono.get(),
                                   self.email.get(), self.cedula.get()]
                    cursor.callproc('spRegistrarCliente', client_data)

                    resultado = 0

                    for result in cursor.stored_results():
                        a = result.fetchall()
                        resultado = a[0]

                    # Imprimir la última fila agregada
                    id_cliente = resultado[0]

                    # Ejecutar el proceso almacenadoe
                    cnx.commit()

                    if id_cliente == 0:
                        print('Cliente registrado')
                    else:
                        print('***** DATOS DEL CLIENTE *****')
                        print('Id Cliente: ' + str(id_cliente))

        elif id_cliente == 0 and self.cedula.get() == '':
            messagebox.showerror(message='Por favor, Ingresar datos del cliente', title='Error de registro')
        else:

            # Obtener datos del pedido
            num_orden = self.num_orden.get()
            fecha_pedido = date.today().strftime("%Y-%m-%d")
            fecha_entrega = self.fecha_entrega.get()
            estado = 'Pendiente'
            observacion_general = self.observacion_general.get()

            metodo_pago = self.combo_metodo.get()

            id_metodo = 0

            if metodo_pago == 'EFECTIVO':
                id_metodo = 1
            if metodo_pago == 'TRANSFERENCIA':
                id_metodo = 2

            abono = self.abono.get()
            total_pagar = self.total.get()
            saldo = self.saldo.get()

            if num_orden == '':
                messagebox.showerror(message='Por favor, Ingresar el número de orden', title='Error de registro')
            elif metodo_pago == '':
                messagebox.showerror(message='Por favor, Ingresar el método de pago', title='Error de registro')
            elif fecha_pedido == '':
                messagebox.showerror(message='Por favor, Ingresar la fecha del pedido', title='Error de registro')
            elif fecha_entrega == '' or fecha_entrega == 'yyyy-mm-dd':
                messagebox.showerror(message='Por favor, Ingresar la fecha de entrega', title='Error de registro')
            elif abono > total_pagar:
                messagebox.showerror(message='El abono no puede ser mayor al total de la venta', title='Error de ingreso')
                self.abono.set(0)
                self.txt_abono.focus()
            elif abono < 0:
                messagebox.showerror(message='El abono no puede ser negativo', title='Error de ingreso')
                self.abono.set(0)
                self.txt_abono.focus()
            elif len(self.prendas_agregadas) == 0:
                messagebox.showerror(message='Por favor, Ingresar prendas / Accesorios', title='Error de registro')
            else:
                fecha_inicio = datetime.datetime.strptime(fecha_pedido, "%Y-%m-%d")
                fecha_fin = datetime.datetime.strptime(fecha_entrega, "%Y-%m-%d")
                if fecha_fin < fecha_inicio:
                    messagebox.showerror(message='La fecha de entrega no debe ser anterior a la actual',
                                         title='Error de Fechas')
                else:
                    if cnx.is_connected():

                        print(".......REGISTRANDO ORDEN CLIENTE......")

                        cursor = cnx.cursor()

                        # Llama al proceso almacenado
                        # To pass the input Arguments create a list and pass it
                        nueva_orden = [id_cliente, num_orden, fecha_pedido,
                                       fecha_entrega, estado,
                                       round(self.saldo.get(), 2), self.total.get(), self.datos_usuario.id, observacion_general]

                        cursor.callproc('spGenerarOrden', nueva_orden)

                        resultado = []

                        for result in cursor.stored_results():
                            a = result.fetchall()
                            resultado = a[0]

                        id_orden = resultado[0]

                        print('---LA ORDEN SE REGISTRO CON EL ID: ' + str(id_orden))

                        print('***** DATOS DEL PEDIDO *****')
                        print('Num.orden: ' + num_orden)
                        print('Fecha_pedido: ' + fecha_pedido)
                        print('Fecha_entrega: ' + fecha_entrega)
                        print('Estado: ' + estado)

                        # Ejecutar el proceso almacenadoe
                        cnx.commit()

                if id_orden != 0:

                    # Obtener prenda agregada
                    print('***** AGREGANDO PRENDAS SELECCIONADAS A LA ORDEN *****')

                    id_tipo_prenda = 0
                    for prenda in self.prendas_agregadas:
                        print(prenda)

                        tipo_servicio = prenda[1]

                        if cnx.is_connected():

                                print(".......INGRESANDO PRENDAS CLIENTE......")

                                cursor = cnx.cursor()

                                # Llama al proceso almacenado
                                # To pass the input Arguments create a list and pass it
                                descripcion_prenda = [prenda[0]]

                                if tipo_servicio == 'PRODUCTO':
                                    cursor.callproc('spObtenerIdProducto', descripcion_prenda)
                                else:
                                    cursor.callproc('spObtenerIdPrenda', descripcion_prenda)

                                resultado = 0

                                for result in cursor.stored_results():
                                    a = result.fetchall()
                                    resultado = a[0]

                                id_tipo_prenda = resultado[0]

                                print('Id prenda: ' + str(id_tipo_prenda))

                                # Ejecutar el proceso almacenadoe
                                cnx.commit()

                                # Obtener el id de cada servicio seleccionado
                                servicio_prenda = [prenda[1]]

                                cursor.callproc('spObtenerIdServicio', servicio_prenda)

                                resultado2 = 0

                                for result in cursor.stored_results():
                                    a = result.fetchall()
                                    resultado2 = a[0]

                                id_tipo_servicio = resultado2[0]

                                print('Id servicio ' + str(id_tipo_servicio))

                                # Obtener el id de cada servicio seleccionado
                                datos_prenda = [id_tipo_prenda, id_tipo_servicio, prenda[2], prenda[4], prenda[5], id_orden]

                                cursor.callproc('spAgregarPrenda', datos_prenda)

                                # Ejecutar el proceso almacenadoe
                                cnx.commit()

                    if cnx.is_connected():

                        print(".......REGISTRANDO PAGO REALIZADO......")

                        cursor = cnx.cursor()

                        # Llama al proceso almacenado
                        # To pass the input Arguments create a list and pass it
                        pago_realizado = [self.abono.get(), id_orden, self.fecha_pedido.get(), id_metodo,
                                          self.datos_usuario.id_caja, self.saldo.get()]

                        cursor.callproc('spRegistrarPago', pago_realizado)

                        resultado = 0

                        for result in cursor.stored_results():
                            a = result.fetchall()
                            resultado = a[0]

                        # Ejecutar el proceso almacenadoe
                        cnx.commit()

                    messagebox.showinfo(message='ORDEN REGISTRADA EXITOSAMENTE!!', title='Generar nueva orden')

                    self.destroy()

                    cnx.close()

                # Obtener empleado a cargo
                print('***** EMPLEADO A CARGO *****')
                print('Id usuario: ' + str(self.datos_usuario.id))

                self.generar_pdf()

    # Obtener el nuevo número de orden
    def obtener_num_orden(self):

        # Conexión a la base de datos Azul lavandería
        db = dbConnection()
        cnx = db.cnx

        nuevo_num_orden = 0

        if cnx.is_connected():

            print("...OBTENIENDO NÚMERO DE ORDEN.....")

            cursor = cnx.cursor()

            # Llama al proceso almacenado
            cursor.callproc('spContarOrdenes')

            for result in cursor.stored_results():
                a = result.fetchall()
                nuevo_num_orden = a[0][0]
                print(nuevo_num_orden)

            self.num_orden.set(nuevo_num_orden)

            cursor.close()
            cnx.close()

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

    def eliminar_prenda(self):

        # Conexión a la base de datos Azul lavandería
        db = dbConnection()
        cnx = db.cnx

        saldo_total = self.saldo.get()

        # Get selected item to Delete
        prenda = self.tabla_prendas.focus()

        selected_item = self.tabla_prendas.selection()[0]
        print(selected_item)
        iid = self.tabla_prendas.index(selected_item)

        print('iid ' + str(iid))

        details = self.tabla_prendas.item(selected_item)

        print(details)

        tipo_servicio = details.get('values')[1]

        precio_eliminar = float(details.get('values')[4])

        print(precio_eliminar)

        self.total_pagar -= precio_eliminar
        saldo_total -= precio_eliminar

        self.total.set(round(self.total_pagar, 2))
        self.saldo.set(round(saldo_total, 2))

        if self.saldo.get() < 0:
            self.saldo.set(0)

        if self.total.get() < 0:
            self.total.set(0)

        if tipo_servicio == 'PRODUCTO':
            print('.....ELIMINANDO PRODCUTO DE LA BD......')

            id_producto = 0
            descripcion = details.get('values')[0]
            cantidad_ingresada = details.get('values')[2]
            precio = details.get('values')[3]
            cantidad_disponible = 0
            stock = 0
            observacion_producto = ''

            cursor = cnx.cursor()

            # Llamar al proceso almacenado
            argumento = [descripcion]
            cursor.callproc('spObtenerIdProducto', argumento)

            for result in cursor.stored_results():
                a = result.fetchall()
                id_producto = a[0][0]
                cantidad_disponible = a[0][1]
                stock = a[0][2]
                observacion_producto = a[0][3]

                print('Id. producto: ' + str(id_producto))
                print('Cantidad disponible: ' + str(cantidad_disponible))

            if id_producto != 0:
                total_productos = cantidad_disponible + cantidad_ingresada

                # Llama al proceso almacenado
                argumento = [id_producto, descripcion, total_productos,
                             stock, precio, observacion_producto]

                cursor.callproc('spActualizarProducto', argumento)

                cnx.commit()

                if cursor.rowcount != 0:
                    messagebox.showinfo(message='Se actualizó correctamente el inventario',
                                         title='Producto devuelto a inventario')

                    self.prendas_agregadas.pop(iid)

                    self.tabla_prendas.delete(selected_item)

                cursor.close()
                cnx.close()
        else:

            self.prendas_agregadas.pop(iid)

            self.tabla_prendas.delete(selected_item)

    def upper_nombres(self, *args):
        self.nombres.set(self.nombres.get().upper())  # change to Upper case

    def upper_direccion(self, *args):
        self.direccion.set(self.direccion.get().upper())  # change to Upper case

    # Validar el tipo de servicio para filtrar los tipos de prenda
    def validar_servicio(self, event):

        # Conexión a la base de datos Azul lavandería
        db = dbConnection()
        cnx = db.cnx

        servicio_seleccionado = self.combo_tipo_serv.get()
        print(servicio_seleccionado)

        self.descripcion_prenda = []

        if cnx.is_connected():

            if servicio_seleccionado != 'PRODUCTO':

                lista_prendas = []

                print("Esperando para obtener prendas")

                cursor = cnx.cursor()

                # Llama al proceso almacenado
                argumento = [servicio_seleccionado]
                cursor.callproc('spObtenerPrendasPorServicio', argumento)

                for result in cursor.stored_results():
                    lista_prendas = result.fetchall()
                    print(lista_prendas)

                i = 1

                self.prendas = []

                for prenda in lista_prendas:
                    self.prendas.append(prenda)
                print(self.prendas)

                # Ejecutar el proceso almacenadoe
                cnx.commit()

                cursor.close()
                cnx.close()

                for prenda in self.prendas:
                    self.descripcion_prenda.append(prenda[0])

                self.combo_tipo_prenda.config(values=self.descripcion_prenda)
            else:
                lista_prendas = []

                print("Esperando para obtener productos")

                cursor = cnx.cursor()

                # Llama al proceso almacenado
                cursor.callproc('spObtenerProductos')

                for result in cursor.stored_results():
                    lista_prendas = result.fetchall()
                    print(lista_prendas)

                i = 1

                self.prendas = []

                for prenda in lista_prendas:
                    self.prendas.append(prenda)
                print(self.prendas)

                # Ejecutar el proceso almacenadoe
                cnx.commit()

                cursor.close()
                cnx.close()

                for prenda in self.prendas:
                    self.descripcion_prenda.append(prenda[1])

                self.combo_tipo_prenda.config(values=self.descripcion_prenda)

        else:
            print("Connection failure")


    def generar_pdf(self):

        fecha_pedido = self.fecha_pedido.get()
        fecha_entrega = self.fecha_entrega.get()
        cedula = self.cedula.get()
        nombres_cliente = self.nombres.get()
        direccion = self.direccion.get()
        telefono = self.telefono.get()

        # Crear el pdf
        pdf = FPDF(orientation="P", unit="cm", format="A4")
        pdf.set_font("helvetica", "", 7)
        pdf.add_page()
        pdf.cell(19, 0.5, "", border=1, ln=1)
        pdf.cell(9, 0.5, "", border=1)
        pdf.cell(6, 0.5, fecha_pedido, border=1, ln=1)
        pdf.cell(9, 0.5, "", border=1)
        pdf.cell(6, 0.5, fecha_entrega, border=1, ln=1)
        pdf.cell(9, 0.5, "", border=1)
        pdf.cell(9, 0.5, nombres_cliente, border=1)
        pdf.cell(2, 0.5, cedula, border=1, ln=1)
        pdf.cell(9, 0.5, "", border=1)
        pdf.cell(9, 0.5, direccion, border=1)
        pdf.cell(2, 0.5, telefono, border=1, ln=1)
        pdf.cell(19, 0.5, "", border=1, ln=1)

        table_data = []

        for prenda in self.prendas_agregadas:
            cadena = [str(item) for item in prenda]
            table_data.append(cadena)
        print(table_data)

        # Posicionar cada item en la factura
        for item in table_data:
            pdf.cell(1, 0.5, item[2], border=1)
            pdf.cell(8,0.5, item[0], border=1)
            pdf.cell(7, 0.5, item[5], border=1)
            pdf.cell(2,0.5, item[3], border=1)
            pdf.cell(2,0.5, item[4], border=1, ln=1)


        total_orden = self.total.get()
        observacion = self.observacion_general.get()

        pdf.set_xy(19, 8)
        pdf.cell(2, 0.5, str(total_orden), border=1, ln=1)
        pdf.set_xy(15, 8.5)
        pdf.cell(6, 0.7, observacion , border=1, ln=1)

        pdf.output("factura.pdf")

        # Imprimir pdf orden de trabajo generada
        pdf_filename = 'factura.pdf'

        # Imprime el pdf del formato para orden generadas
        os.startfile(pdf_filename,'print')





