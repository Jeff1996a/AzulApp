import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
from tkcalendar import *
from datetime import date

from dbConnection import dbConnection

class ActualizarOrden(tk.Toplevel):

    def __init__(self, datos_usuario):

        super().__init__()

        # Obtener datos del usuario registrado
        self.datos_usuario = datos_usuario

        print('El id del usuario ' + str(self.datos_usuario.id))

        # Variable asociadas a cada campo de la prenda
        self.tipo_prenda = tk.StringVar()
        self.tipo_servicio = tk.StringVar()
        self.observacion = tk.StringVar()
        self.cantidad = tk.IntVar()

        # Tipo de pago
        self.tipo_pago = tk.StringVar()

        # Conexión a la base de datos Azul lavandería
        self.db = dbConnection()
        self.cnx = self.db.cnx

        #Vector para obtener datos de la orden
        self.datos_orden = []

        self.lblTitulo = ttk.Label(self, text='Azul Lavandería', font=('Courier', 20), foreground='blue')
        self.lblTitulo.pack(side='top', padx=10, pady=3)

        # Pregunta de bienvenida
        self.lbl_registrar_pedido= ttk.Label(self, text='Registrar entrega de pedido ', font=('Courier', 15),
                                       foreground='purple')
        self.lbl_registrar_pedido.pack(side='top', anchor='center', padx=10, pady=0)

        # Fila 1
        self.frame1 = tk.Frame(self)
        self.frame1.pack(side='top', fill='both', padx=10, pady=4)

        # *********************************** CONTENEDOR CLIENTE **********************************************

        # Frame cliente
        self.cliente_container = tk.LabelFrame(self.frame1, text='DATOS CLIENTE', font=("Courier", 12),
                                               foreground='green')
        self.cliente_container.pack(side='left', fill='both', ipadx=5, ipady=0)

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
        self.lblcedula = ttk.Label(self.cedula_container, text='CÉDULA/PASAPORTE:', font=("Courier", 10), width=20)
        self.lblcedula.pack(side='left', anchor='nw', padx=0, pady=2, ipadx=2, ipady=2)

        # Text cédula del cliente
        self.txtCedula = ttk.Entry(self.cedula_container, width=30)
        self.txtCedula.pack(side='left', padx=0, pady=2, ipadx=2, ipady=2)
        self.txtCedula.config(state='readonly')

        # Contenedor para los nombres del cliente
        self.nombres_container = tk.Frame(self.cliente_container)
        self.nombres_container.pack(side="top", fill='both')

        # Label nombres del cliente
        self.lblname = ttk.Label(self.nombres_container, text='APELLIDOS Y NOMBRES:', font=("Courier", 10), width=20)
        self.lblname.pack(side='left', anchor='nw', padx=0, pady=2, ipadx=2, ipady=2)

        # Text nombres del cliente
        self.txtnombre = ttk.Entry(self.nombres_container, width=30)
        self.txtnombre.pack(side='left', padx=0, pady=2, ipadx=2, ipady=2)
        self.txtnombre.config(state='readonly')

        # Contenedor para la dirección del cliente
        self.direccion_container = tk.Frame(self.cliente_container)
        self.direccion_container.pack(side="top", fill='both')

        # Label direccion del cliente
        self.lbldireccion = ttk.Label(self.direccion_container, text='DIRECCIÓN:', font=("Courier", 10), width=20)
        self.lbldireccion.pack(side='left', anchor='nw', padx=0, pady=2, ipadx=2, ipady=2)

        # Text direccion del cliente
        self.txtDireccion = ttk.Entry(self.direccion_container, width=30)
        self.txtDireccion.pack(side='left', padx=0, pady=2, ipadx=2, ipady=2)
        self.txtDireccion.config(state='readonly')

        # Contenedor teléfono del cliente
        self.telefono_container = tk.Frame(self.cliente_container)
        self.telefono_container.pack(side="top", fill='both')

        # Label telefono del cliente
        self.lblTelefono = ttk.Label(self.telefono_container, text='TELÉFONO:', font=("Courier", 10), width=20)
        self.lblTelefono.pack(side='left', anchor='nw', padx=0, pady=2, ipadx=2, ipady=2)

        # Text telefono del cliente
        self.txtTelefono = ttk.Entry(self.telefono_container, width=30)
        self.txtTelefono.pack(side='left', padx=0, pady=2, ipadx=2, ipady=2)
        self.txtTelefono.config(state='readonly')

        # Contenedor email del cliente
        self.email_container = tk.Frame(self.cliente_container)
        self.email_container.pack(side="top", fill='both')

        # Label telefono del cliente
        self.lblEmail = ttk.Label(self.email_container, text='CORREO ELECTRÓNICO:', font=("Courier", 10), width=20)
        self.lblEmail.pack(side='left', anchor='nw', padx=0, pady=2, ipadx=2, ipady=2)

        # Text telefono del cliente
        self.txtEmail = ttk.Entry(self.email_container, width=30)
        self.txtEmail.pack(side='left', padx=0, pady=2, ipadx=2, ipady=2)
        self.txtEmail.config(state='readonly')

        # ******************************************************DETALLES DE PEDIDO****************************
        # Lista de metodos de pago
        self.metodos = []

        self.obtener_metodos_pago()

        self.descripcion_metodos = []

        for metodo in self.metodos:
            self.descripcion_metodos.append(metodo[0])
        # Contenedor detalles orden
        self.orden_container = tk.LabelFrame(self.frame1, text='DETALLES DEL PEDIDO', font=("Courier", 12),
                                             foreground='green')
        self.orden_container.pack(side='right', fill='both')

        # Número de orden container
        self.num_order_container = tk.Frame(self.orden_container)
        self.num_order_container.pack(side='top', fill='both', ipadx=2, ipady=0, padx=0, pady=2)

        # Label número de orden
        self.lbl_num_order = ttk.Label(self.num_order_container, text='ORDEN N°:', font=("Courier", 10), width=15,
                                       foreground='purple')
        self.lbl_num_order.pack(side='left', anchor='nw', padx=0, pady=2, ipadx=2, ipady=2)

        # Text número de orden
        self.txt_num_order = ttk.Entry(self.num_order_container, width=15)
        self.txt_num_order.pack(side='left', padx=0, pady=2, ipadx=2, ipady=2)
        self.txt_num_order.focus()

        self.txt_num_order.bind('<FocusOut>', self.obtener_orden)

        # Contenedor método de pago
        self.contenedor_metodo = ttk.Frame(self.orden_container)
        self.contenedor_metodo.pack(side='top', fill='both', ipadx=3, ipady=0, padx=0, pady=0)

        # Label tipo de servicio
        self.label_metodo = ttk.Label(self.contenedor_metodo, text='MÉTODO PAGO:', font=("Courier", 10), width=15)
        self.label_metodo.pack(side='left', padx=0, pady=2, ipadx=2, ipady=2)

        # Combo método de pago
        self.combo_metodo = ttk.Combobox(self.contenedor_metodo, width=11,
                                         values=self.descripcion_metodos, font=("Courier", 8),
                                         textvariable=self.tipo_pago)
        self.combo_metodo.pack(side='left', padx=0, pady=2, ipadx=0, ipady=0)

        # Estado de orden container
        self.estado_orden_container = tk.Frame(self.orden_container)
        self.estado_orden_container.pack(side='top', fill='both', ipadx=2, ipady=0, padx=0, pady=2)

        # Label número de orden
        self.lbl_estado = ttk.Label(self.estado_orden_container, text='ESTADO:', font=("Courier", 10), width=15)
        self.lbl_estado.pack(side='left', anchor='nw', padx=0, pady=2, ipadx=2, ipady=2)

        # Text número de orden
        self.txt_estado = ttk.Entry(self.estado_orden_container, width=15)
        self.txt_estado.pack(side='left', padx=0, pady=2, ipadx=2, ipady=2)
        self.txt_estado.config(state='readonly')

        # Fecha de entrada
        self.fecha_orden_container = tk.Frame(self.orden_container)
        self.fecha_orden_container.pack(side='top', fill='both', ipadx=2, ipady=0, padx=0, pady=2)

        # Label fecha de entrada
        self.lbl_fecha_order = ttk.Label(self.fecha_orden_container, text='FECHA PEDIDO:', font=("Courier", 10),
                                         width=15)
        self.lbl_fecha_order.pack(side='left', anchor='nw', padx=0, pady=2, ipadx=2, ipady=2)

        # Text fecha de entrada
        self.txt_fecha_order = ttk.Entry(self.fecha_orden_container, width=15)
        self.txt_fecha_order.pack(side='left', padx=0, pady=2, ipadx=2, ipady=2)
        self.txt_fecha_order.config(state='readonly')

        # Fecha de entrega
        self.fecha_entrega_container = tk.Frame(self.orden_container)
        self.fecha_entrega_container.pack(side='top', fill='both', ipadx=2, ipady=0, padx=0, pady=2)

        # Label fecha de entrada
        self.lbl_fecha_entrega = ttk.Label(self.fecha_entrega_container, text='FECHA ENTREGA:', font=("Courier", 10),
                                           width=15)
        self.lbl_fecha_entrega.pack(side='left', anchor='nw', padx=0, pady=2, ipadx=2, ipady=2)

        # Text fecha de entrada
        self.txt_fecha_entrega = ttk.Entry(self.fecha_entrega_container, width=15)
        self.txt_fecha_entrega.pack(side='left', padx=0, pady=2, ipadx=2, ipady=2)
        self.txt_fecha_entrega.insert(0, "yyyy/dd/mm")

        # Calendario de fecha entrada
        self.date_frame = tk.Frame(self.orden_container)

        self.cal = Calendar(self.date_frame, selectmode='day', date_pattern='y-mm-dd')

        self.submit_date = ttk.Button(self.date_frame, text='INGRESAR', width=15, command=self.grab_date)
        self.txt_fecha_entrega.bind('<1>', self.pick_date)

        # ******************************************************************************************************
        # Contenedor tabla prendas
        self.contenedor_tabla = tk.LabelFrame(self, text='PRENDAS / ACCESORIOS', font=("Courier", 12),
                                              foreground='green')
        self.contenedor_tabla.pack(side='top', fill='both', padx=10, pady=0)

        # Contenedor del botón para agregar mas prendas
        self.contenedor_btn_agregar = tk.Frame(self.contenedor_tabla)
        self.contenedor_btn_agregar.pack(side='top', fill='both')

        # ***********************************************************************************************************
        self.contenedor_frm_agregar_item = tk.Frame(self.contenedor_tabla)
        self.contenedor_frm_agregar_item.pack(side='top', fill='both', padx=10, pady=0)

        # contenedor lista de prendas
        self.encabezado = ('#1', '#2', '#3', '#4', '#5', '#6', '#7')
        self.tabla_prendas = ttk.Treeview(self.contenedor_tabla, columns=self.encabezado, show='headings', height=4)
        self.tabla_prendas.pack(side='top', fill='both', padx=10, pady=10)

        self.tabla_prendas.column('#1', width=25, minwidth=25, stretch=False)
        self.tabla_prendas.column('#2', width=200, minwidth=200, stretch=False)
        self.tabla_prendas.column('#3', width=130, minwidth=130, stretch=False)
        self.tabla_prendas.column('#4', width=50, minwidth=50, stretch=False)
        self.tabla_prendas.column('#5', width=50, minwidth=50, stretch=False)
        self.tabla_prendas.column('#6', width=50, minwidth=50, stretch=False)
        self.tabla_prendas.column('#7', width=170, minwidth=170, stretch=False)

        self.tabla_prendas.heading('#1', text="N°")
        self.tabla_prendas.heading('#2', text='PRENDA/ACCESORIO')
        self.tabla_prendas.heading('#3', text='TIPO DE SERVICIO')
        self.tabla_prendas.heading('#4', text='CANT.')
        self.tabla_prendas.heading('#5', text='PRECIO')
        self.tabla_prendas.heading('#6', text='TOTAL')
        self.tabla_prendas.heading('#7', text='OBSERVACIONES')

        # Contenedor para los abonos, saldos y totales
        self.total = tk.DoubleVar()
        self.saldo = tk.DoubleVar()
        self.abono = tk.DoubleVar()

        self.contenedor_saldos = tk.LabelFrame(self, text='ABONOS Y SALDOS', font=("Courier", 12), foreground='green')
        self.contenedor_saldos.pack(side='top', fill='both', padx=10, pady=0, ipadx=5, ipady=5)

        # Mensaje de abonos realizados
        self.msg_abono = tk.StringVar()

        self.label_abonos_realizados = ttk.Label(self.contenedor_saldos, text='', foreground='orange', textvariable=self.msg_abono, font=("Courier", 10))
        self.label_abonos_realizados.pack(side='top')


        # Abono cliente
        self.abono_container = tk.Frame(self.contenedor_saldos)
        self.abono_container.pack(side='left', anchor='w', ipadx=2, ipady=0, padx=0, pady=2)

        # Label abono cliente
        self.lbl_abono = ttk.Label(self.abono_container, text='IMPORTE ($):', font=("Courier", 12),
                                   foreground='purple')
        self.lbl_abono.pack(side='left', padx=0, pady=2, ipadx=2, ipady=2)

        # Text abono cliente
        self.txt_abono = ttk.Entry(self.abono_container, width=8, font=("Arial", 13))
        self.txt_abono.pack(side='left', padx=0, pady=2, ipadx=2, ipady=2, )

        self.txt_abono['textvariable'] = self.abono
        self.abono.set(0.0)

        # Saldo cliente
        self.saldo_container = tk.Frame(self.contenedor_saldos)
        self.saldo_container.pack(side='left', anchor='center', ipadx=2, ipady=0, padx=0, pady=2)

        # Label saldo cliente
        self.lbl_saldo = ttk.Label(self.saldo_container, text='SALDO ($):', font=("Courier", 12),
                                   foreground='blue')
        self.lbl_saldo.pack(side='left', padx=0, pady=2, ipadx=2, ipady=2)

        # Text saldo cliente
        self.txt_saldo = ttk.Entry(self.saldo_container, width=8, font=("Arial", 13))
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
        self.txt_total = ttk.Entry(self.total_container, width=8, font=("Arial", 13))
        self.txt_total.pack(side='left', padx=0, pady=2, ipadx=2, ipady=2)
        self.txt_total.config(state='readonly')

        self.txt_total['textvariable'] = self.total

        self.total.set(0.0)

        # ************************************************************************************************************

        # Contenedor observaciones generales
        self.contenedor_observaciones = tk.LabelFrame(self, text='OBSERVACIONES GENERALES', font=("Courier", 12),
                                                      foreground='green')
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
            text="REGISTRAR ENTREGA",
            command=self.actualizar_orden,
            image=self.save,
            compound='right',
        )
        self.guardar_button.pack(side='left', anchor='center', padx=10, pady=10, ipadx=5, ipady=3)

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
        self.cancelar_registro.pack(side='right', anchor='center', padx=10, pady=10, ipadx=5, ipady=3)

        # Variables datos del cliente
        self.idCliente = tk.StringVar()
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
        self.estado = tk.StringVar()
        self.observacion_general = tk.StringVar()

        self.txt_num_order['textvariable'] = self.num_orden
        self.txt_fecha_order['textvariable'] = self.fecha_pedido
        self.txt_fecha_entrega['textvariable'] = self.fecha_entrega
        self.txt_estado['textvariable'] = self.estado
        self.txt_observaciones['textvariable'] = self.observacion_general

        self.fecha_pedido.set("yyyy-mm-dd")
        self.fecha_entrega.set('yyyy-mm-dd')

        # Prendas agregadas
        self.prendas_agregadas = []

        self.focus()

        self.grab_set()

    def pick_date(self, event):
        self.date_frame.pack(side='top')
        self.cal.pack(side='top')
        self.submit_date.pack(side='top')

    def grab_date(self):
        self.txt_fecha_entrega.delete(0, 'end')
        self.txt_fecha_entrega.insert(0, self.cal.get_date())
        self.date_frame.pack_forget()

    def obtener_orden(self, event):

        orden_obtenida=[]

        if self.cnx.is_connected():

            print(".....OBTENIENDO INFORMACIÓN DE LA ORDEN DE TRABAJO.....")

            cursor = self.cnx.cursor()

            # Llama al proceso almacenado
            argument = [self.num_orden.get()]
            cursor.callproc('spObtenerOrden', argument)

            for result in cursor.stored_results():
                orden_obtenida = result.fetchall()
                print(orden_obtenida)

            if len(orden_obtenida) != 0:

                self.datos_orden = orden_obtenida[0]

                print(self.datos_orden)

                print(".....OBTENIENDO DATOS DE LA ORDEN DE TRABAJO.....")

                id_orden = self.datos_orden[0]

                fecha_pedido = self.datos_orden[3].strftime("%Y-%m-%d")
                fecha_entrega = self.datos_orden[4].strftime("%Y-%m-%d")

                estado = self.datos_orden[5]

                saldo = round(self.datos_orden[6], 2)
                total = self.datos_orden[7]
                observaciones = self.datos_orden[8]

                # Validar el estado de la orden
                if estado == 'PENDIENTE':
                    self.txt_estado.config(foreground='red')
                elif estado == 'ENTREGADO':
                    self.txt_estado.config(foreground='blue')

                print('id orden: ' + str(id_orden))
                print('fecha pedido: ' + fecha_pedido)
                print('fecha entrega: ' + fecha_entrega)
                print('Estado: ' + estado)

                print('Saldo: ' + str(saldo))
                print('Total a pagar: ' + str(total))

                self.fecha_pedido.set(fecha_pedido)
                self.fecha_entrega.set(fecha_entrega)
                self.estado.set(estado)
                self.saldo.set(saldo)
                self.total.set(total)
                self.observacion_general.set(observaciones)

                print(".....OBTENIENDO DATOS DEL CLIENTE.....")

                id_cliente = self.datos_orden[1]

                print('id cliente: ' + str(id_cliente))

                if self.cnx.is_connected():

                    cliente_encontrados=[]

                    # Llama al proceso almacenado
                    # To pass the input Arguments create a list and pass it
                    buscador = [id_cliente, ]
                    cursor.callproc('spObtenerClientePorId', buscador)

                    for result in cursor.stored_results():
                        cliente_encontrados = result.fetchall()
                        print(cliente_encontrados)

                    cliente = cliente_encontrados[0]
                    print(cliente)

                    # Asignar datos obtenidos a los cuadros de texto
                    self.idCliente.set(id_cliente)
                    self.nombres.set(cliente[1])
                    self.direccion.set(cliente[2])
                    self.telefono.set(cliente[3])
                    self.email.set(cliente[4])
                    self.cedula.set(cliente[5])

                    # Ejecutar el proceso almacenadoe
                    self.cnx.commit()

                else:
                    print("Connection failure")

                print('..... OBTENER LAS PRENDAS REGISTRADAS....')
                if self.cnx.is_connected():

                    prendas_agregadas=[]

                    for row in self.tabla_prendas.get_children():
                        self.tabla_prendas.delete(row)

                    # Llama al proceso almacenado
                    # To pass the input Arguments create a list and pass it
                    buscador = [id_orden, ]
                    cursor.callproc('spObtenerPrendasPorPedido', buscador)

                    for result in cursor.stored_results():
                        prendas_agregadas = result.fetchall()
                        print(prendas_agregadas)

                    i = 0

                    # Agregar a la lista de prendas
                    for prenda in prendas_agregadas:
                        i += 1
                        item = (i, prenda[1], prenda[2], prenda[3], prenda[4], prenda[5], prenda[6])
                        self.tabla_prendas.insert("", 'end', iid=prenda[0],
                                                  values=item)

                    # Ejecutar el proceso almacenadoe
                    self.cnx.commit()

                else:
                    print("Connection failure")

                print('..... OBTENER LOS PAGOS REALIZADOS....')
                self.obtener_importe(id_orden)
            else:
                messagebox.showerror(message='¡NO SE ENCONTRÓ NINGUNA ORDEN!', title='Error de busqueda')
                print('NO SE ENCONTRÓ NINGÚN REGISTRO')

            # Ejecutar el proceso almacenadoe
            self.cnx.commit()

        else:
            print("Connection failure")

    def actualizar_orden(self):

        print('....ACTUALIZANDO LA ENTREGA DEL PEDIDO.....')

        print(".....OBTENIENDO DATOS DE LA ORDEN DE TRABAJO.....")

        id_orden = self.datos_orden[0]

        fecha_pedido = self.datos_orden[3].strftime("%Y-%m-%d")
        fecha_entrega = self.fecha_entrega.get()
        estado = self.estado.get()
        metodo = self.combo_metodo.get()

        id_metodo = 0

        if metodo == 'EFECTIVO':
            id_metodo = 1
        if metodo == 'TRANSFERENCIA':
            id_metodo = 2


        abono = self.abono.get()
        saldo = self.saldo.get()
        total = self.total.get()
        observaciones = self.observacion_general.get()

        # Validar el estado de la orden
        if estado == 'PENDIENTE':
            self.txt_estado.config(foreground='red')

        print('id orden: ' + str(id_orden))
        print('fecha pedido: ' + fecha_pedido)
        print('fecha entrega: ' + fecha_entrega)
        print('Estado: ' + estado)
        print('Método de pago: ' + metodo)

        print('Abono: ' + str(abono))
        print('Saldo: ' + str(saldo))
        print('Total a pagar: ' + str(total))

        self.fecha_pedido.set(fecha_pedido)
        self.fecha_entrega.set(fecha_entrega)
        self.estado.set(estado)
        self.abono.set(abono)
        self.saldo.set(saldo)
        self.total.set(total)
        self.observacion_general.set(observaciones)

        print(".....OBTENIENDO DATOS DEL CLIENTE.....")

        id_cliente = self.datos_orden[1]
        print('id cliente: ' + str(id_cliente))

        # Obtener empleado a cargo
        print('***** EMPLEADO A CARGO *****')
        print('Id usuario: ' + str(self.datos_usuario.id))

        if estado == 'PENDIENTE':

            if fecha_entrega != date.today().strftime("%Y-%m-%d"):
                messagebox.showerror(message='LA FECHA DE ENTREGA NO COINCIDE CON LA ACTUAL!!', title='Error de fecha')
            elif abono == 0 and saldo > 0:
                messagebox.showerror(message='LA ORDEN TIENE UN SALDO PENDIENTE!!', title='Error de registro')
            elif abono > saldo:
                messagebox.showerror(message='EL IMPORTE NO DEBE SER MAYOR AL SALDO!!', title='Error de registro')
            elif abono != saldo:
                messagebox.showerror(message='INGRESAR EL VALOR PENDIENTE DEL CLIENTE!!', title='Error de registro')
            elif abono < 0:
                messagebox.showerror(message='EL IMPORTE NO DEBE SER NEGATIVO!!', title='Error de registro')
            elif metodo == '':
                messagebox.showerror(message='INGRESAR EL MÉTODO DE PAGO!!', title='Error de registro')
            else:
                self.saldo.set(0)

                if self.cnx.is_connected():

                    print(".....ACTUALIZANDO INFORMACIÓN DE LA ORDEN DE TRABAJO.....")

                    cursor = self.cnx.cursor()

                    # Llama al proceso almacenado
                    # To pass the input Arguments create a list and pass it
                    actualizar_orden = [id_orden, id_cliente, fecha_pedido,
                                        fecha_entrega, 'ENTREGADO', round(self.saldo.get(), 2),
                                        self.total.get(), self.datos_usuario.id, observaciones]
                    cursor.callproc('spActualizarOrden', actualizar_orden)

                    for result in cursor.stored_results():
                        a = result.fetchall()
                        print(a)

                    # Ejecutar el proceso almacenadoe
                    self.cnx.commit()

                    if cursor.rowcount != 0:
                        self.estado.set('ENTREGADO')

                        if self.cnx.is_connected():

                            print(".......REGISTRANDO PAGO REALIZADO......")

                            cursor = self.cnx.cursor()

                            # Llama al proceso almacenado
                            # To pass the input Arguments create a list and pass it
                            pago_realizado = [self.abono.get(), id_orden, self.fecha_pedido.get(), id_metodo,
                                              self.datos_usuario.id_caja, 0]

                            cursor.callproc('spRegistrarPago', pago_realizado)

                            resultado = 0

                            for result in cursor.stored_results():
                                a = result.fetchall()
                                resultado = a[0]

                            # Ejecutar el proceso almacenadoe
                            self.cnx.commit()
                        messagebox.showinfo(message='ENTREGA REGISTRADA EXITOSAMENTE!!', title='Entregar pedido')
                        self.destroy()
                else:
                    print("Connection failure")

        else:
            messagebox.showerror(message='LA ORDEN YA FUE ENTREGADA!!', title='Pedido entregado')

    # Función para obtener los métodos de pago disponibles
    def obtener_metodos_pago(self):

        lista_metodos = []

        if self.cnx.is_connected():

            print("....OBTENIENDO MÉTODOS DE PAGO.....")

            cursor = self.cnx.cursor()

            # Llama al proceso almacenado
            cursor.callproc('spObtenerMetodosPago')

            for result in cursor.stored_results():
                lista_metodos = result.fetchall()
                print(lista_metodos)

            self.metodos = []

            for metodo in lista_metodos:
                self.metodos.append(metodo)
            print(self.metodos)

        else:
            print("Connection failure")

    def obtener_importe(self, id_orden):
        if self.cnx.is_connected():

            pagos_encontrados = []

            cursor = self.cnx.cursor()

            # Llama al proceso almacenado
            # To pass the input Arguments create a list and pass it
            buscador = [id_orden, ]

            cursor.callproc('spObtenerPagosPorOrden', buscador)

            for result in cursor.stored_results():
                pagos_encontrados = result.fetchall()
                print(pagos_encontrados)

            # Ejecutar el proceso almacenadoe
            self.cnx.commit()

            if len(pagos_encontrados) != 0:

                total_abonos = 0
                saldo = self.saldo.get()

                for pago in pagos_encontrados:
                    if pago[1] == 0:
                        self.msg_abono.set('Cuenta con un abono de: 0.00 $')
                    elif saldo == 0:
                        self.msg_abono.set('La orden ya fue entregada')
                        self.label_abonos_realizados.config(foreground='green')
                    else:
                        total_abonos += pago[1]
                        self.msg_abono.set('Cuenta con un abono de: ' + str(total_abonos) + '$ realizado el: ' +
                                           pago[2].strftime("%Y-%m-%d") + ' con: ' + pago[3])
            else:
                self.msg_abono.set('')
        else:
            print("Connection failure")
