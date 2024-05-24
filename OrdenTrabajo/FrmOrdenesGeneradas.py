import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
from tkcalendar import *
from datetime import date

from dbConnection import dbConnection

class ListaOrdenes(tk.Toplevel):

    def __init__(self, datos_usuario):
        super().__init__()

        # Array para cargar la lista de ordenes
        self.lista_ordenes = []

        # Variables para llevar el control de las ordenes generadas
        self.total_ordenes = tk.IntVar()
        self.total_pendientes = tk.IntVar()
        self.total_entregadas = tk.IntVar()

        self.total_generado = tk.DoubleVar()
        self.total_abonos = tk.DoubleVar()
        self.total_saldo = tk.DoubleVar()

        self.total_transferencias = tk.DoubleVar()
        self.total_efectivo = tk.DoubleVar()

        # Conexión a la base de datos Azul lavandería
        self.db = dbConnection()
        self.cnx = self.db.cnx

        self.lblTitulo = ttk.Label(self, text='Azul Lavandería', font=('Courier', 20), foreground='blue')
        self.lblTitulo.pack(side='top', padx=10, pady=0)

        # Pregunta de bienvenida
        self.lblNuevaOrden = ttk.Label(self, text='Registro ordenes de trabajo ', font=('Courier', 15),
                                       foreground='purple')
        self.lblNuevaOrden.pack(side='top', anchor='center', padx=10, pady=0)

        # TABLA ORDENES DE TRABAJO

        self.contenedor_tabla = tk.LabelFrame(self, text='ORDENES DE TRABAJO GENERADAS', font=('Courier', 15), foreground='green')
        self.contenedor_tabla.pack(side='top', fill='both', padx=5, pady=5)

        # Contenedor buscar ordenes por fecha
        self.contenedor_filto = ttk.Frame(self.contenedor_tabla)
        self.contenedor_filto.pack(side='top', fill='both', padx=5, pady=5)

        # Contenedor buscar ordenes por fecha
        self.contenedor_buscar = ttk.Frame(self.contenedor_filto)
        self.contenedor_buscar.pack(side='top', fill='both', padx=0, pady=0)

        # Label para el contenedor buscar
        self.lbl_buscar = ttk.Label(self.contenedor_buscar, text='Fecha pedido:', font=('Courier', 10) )
        self.lbl_buscar.pack(side='left', anchor='w', padx=0, pady=0, ipadx=0, ipady=2)

        # Entry para el contenedor buscar
        self.buscar = tk.StringVar()

        self.txt_buscar = ttk.Entry(self.contenedor_buscar, width=30)
        self.txt_buscar.pack(side='left', padx=2, pady=0)

        self.txt_buscar['textvariable'] = self.buscar

        # Create an object of tkinter ImageTk
        self.readImg = Image.open("Img/search.png")
        self.newImg = self.readImg.resize((15, 15))
        self.img = ImageTk.PhotoImage(self.newImg)

        # Botón para guardar los datos
        self.buscar_button = ttk.Button(
            self.contenedor_buscar,
            image=self.img,
            command=self.filtrar_tablas,
            compound='right',
            width=3,
        )
        self.buscar_button.pack(side='left', anchor='center', ipadx=2, ipady=0, padx=2)

        # Calendario de fecha entrada
        self.contenedor_calendario = tk.Frame(self.contenedor_tabla)

        self.date_frame = tk.Frame(self.contenedor_calendario)
        self.date_frame.pack(side='left', fill='both')

        self.cal = Calendar(self.date_frame, selectmode='day', date_pattern='y-mm-dd')

        self.submit_date = ttk.Button(self.date_frame, text='INGRESAR', width=15, command=self.grab_date)
        self.txt_buscar.bind('<1>', self.pick_date)

        self.buscar.set(date.today().strftime("%Y-%m-%d"))

        # Treeview para las ordenes generadas
        self.encabezado = ('#1', '#2', '#3', '#4', '#5', '#6', '#7', '#8', '#9', '#10')
        self.tabla_ordenes = ttk.Treeview(self.contenedor_tabla, columns=self.encabezado, show='headings')
        self.tabla_ordenes.pack(side='bottom', fill='both', padx=5, pady=5)

        self.tabla_ordenes.column('#1', width=25, minwidth=25, stretch=False)
        self.tabla_ordenes.column('#2', width=80, minwidth=80, stretch=False)
        self.tabla_ordenes.column('#3', width=100, minwidth=100, stretch=False)
        self.tabla_ordenes.column('#4', width=150, minwidth=150, stretch=False)
        self.tabla_ordenes.column('#5', width=80, minwidth=80, stretch=False)
        self.tabla_ordenes.column('#6', width=100, minwidth=100, stretch=False)
        self.tabla_ordenes.column('#7', width=100, minwidth=100, stretch=False)
        self.tabla_ordenes.column('#8', width=80, minwidth=80, stretch=False)
        self.tabla_ordenes.column('#9', width=80, minwidth=80, stretch=False)
        self.tabla_ordenes.column('#10', width=120, minwidth=120, stretch=False)

        self.tabla_ordenes.heading('#1', text="N°")
        self.tabla_ordenes.heading('#2', text='NUM. ORDEN')
        self.tabla_ordenes.heading('#3', text='FECHA PEDIDO')
        self.tabla_ordenes.heading('#4', text='CLIENTE')
        self.tabla_ordenes.heading('#5', text='TELÉFONO')
        self.tabla_ordenes.heading('#6', text='FECHA ENTREGA')
        self.tabla_ordenes.heading('#7', text='ESTADO')
        self.tabla_ordenes.heading('#8', text='SALDO ($)')
        self.tabla_ordenes.heading('#9', text='TOTAL ($)')
        self.tabla_ordenes.heading('#10', text='RESPONSABLE')

        self.obtener_ordenes()

        # ************************************************************************************

        # Contenedor detalle ordenes
        self.contenedor_detalles = tk.LabelFrame(self, text='RESUMEN GENERAL DEL DÍA', font=('Courier', 13), foreground='green')
        self.contenedor_detalles.pack(side='bottom', fill='both', padx=5, pady=5, ipadx=5, ipady=10)

        # Contenedor total ordenes
        self.contenedor_total_ordenes = tk.Frame(self.contenedor_detalles)
        self.contenedor_total_ordenes.pack(side='left', anchor='w', fill='both', padx=10, pady=5)

        self.label_total_ordenes = ttk.Label(self.contenedor_total_ordenes, text='Ordenes generadas: ',
                                             font=('Courier', 11), width=20)
        self.label_total_ordenes.pack(side='left', anchor='w')

        self.txt_total_ordenes = ttk.Entry(self.contenedor_total_ordenes, textvariable=self.total_ordenes, width=10)
        self.txt_total_ordenes.pack(side='left', padx=2, pady=0)
        self.txt_total_ordenes.config(state='readonly')

        # Contenedor total de saldos pendientes
        self.contenedor_total_saldos = tk.Frame(self.contenedor_detalles)
        self.contenedor_total_saldos.pack(side='left', fill='both',anchor='center', padx=10, pady=5)

        self.label_total_saldos = ttk.Label(self.contenedor_total_saldos, text='Total saldos($): ',
                                                font=('Courier', 11), width=20)
        self.label_total_saldos.pack(side='left', anchor='w')

        self.txt_total_saldos = ttk.Entry(self.contenedor_total_saldos, textvariable=self.total_saldo, width=10)
        self.txt_total_saldos.pack(side='left', padx=2, pady=0)
        self.txt_total_saldos.config(state='readonly')

        # Contenedor Total ventas realizadas
        self.contenedor_total_ventas = tk.Frame(self.contenedor_detalles)
        self.contenedor_total_ventas.pack(side='left', fill='both', anchor='e', padx=10, pady=5)

        self.label_total_ventas = ttk.Label(self.contenedor_total_ventas, text='Total ventas ($): ',
                                                font=('Courier', 11), width=20)
        self.label_total_ventas.pack(side='left', anchor='w')

        self.txt_total_ventas = ttk.Entry(self.contenedor_total_ventas, textvariable=self.total_generado, width=10)
        self.txt_total_ventas.pack(side='left', padx=2, pady=0)
        self.txt_total_ventas.config(state='readonly')

        self.focus()
        self.grab_set()

    def obtener_ordenes(self):

        orden_obtenida=[]

        if self.cnx.is_connected():

            print(".....OBTENIENDO INFORMACIÓN DE LA ORDEN DE TRABAJO.....")

            cursor = self.cnx.cursor()

            # Parametros del proceso almacenado
            parametros = [self.buscar.get(),]

            # Llama al proceso almacenado
            cursor.callproc('spObtenerOrdenes', parametros)

            for result in cursor.stored_results():
                orden_obtenida = result.fetchall()
                print(orden_obtenida)

            i = 0

            total_saldos = 0

            total_generado = 0

            # Agregar cada orden obtenida al treeview
            for orden in orden_obtenida:
                i += 1
                id_orden = orden[0]
                num_orden = orden[1]
                fecha_pedido = orden[2].strftime("%Y-%m-%d")
                fecha_entrega = orden[3].strftime("%Y-%m-%d")
                estado = orden[4]
                saldo = orden[5]
                total = orden[6]
                nombre_cliente = orden[7]
                cedula = orden[8]
                telefono = orden[9]
                email = orden[10]
                responsable = orden[11] + ' ' + orden[12]

                print('..... DETALLES DE LA ORDEN N°: ' + str(num_orden) + '......')
                print ('id_orden : ' + str(id_orden))
                print('fecha pedido : ' + fecha_pedido)
                print('fecha entrega : ' + fecha_entrega)
                print('Estado : ' + estado)
                print('Saldo:' + str(saldo))
                print('Total a pagar: ' + str(total))
                print('Cliente: ' + nombre_cliente)
                print('Cédula: ' + cedula)
                print('Teléfono: ' + telefono)
                print('Correo: ' + email)
                print('Responsable:' + responsable)

                total_saldos += saldo
                total_generado += total


                detalle_orden = (i, num_orden,fecha_pedido, nombre_cliente, telefono, fecha_entrega, estado, saldo, total,  responsable )

                self.tabla_ordenes.insert("", 'end', iid=id_orden,
                                          values=detalle_orden)

            self.total_ordenes.set(i)
            self.total_saldo.set(total_saldos)
            self.total_generado.set(total_generado)


            print('ORDENES GENERADAS: ' + str(self.total_ordenes))
            print('ORDENES PENDIENTES: ' + str(self.total_pendientes))
            print('ORDENES ENTREGADAS: ' + str(self.total_entregadas))
            self.cnx.commit()
        else:
            print("Connection failure")

    # Mostrar pop up date
    def pick_date(self, event):
        self.contenedor_calendario.pack(side='top', fill='both')
        self.cal.pack(side='top')
        self.submit_date.pack(side='top')

    # Recolectar fecha
    def grab_date(self):
        self.txt_buscar.delete(0, 'end')
        self.txt_buscar.insert(0, self.cal.get_date())
        self.contenedor_calendario.pack_forget()
        self.filtrar_tablas()

    # Filtar los datos de la fecha
    def filtrar_tablas(self):

        # Limpiar la tabla
        for i in self.tabla_ordenes.get_children():
            self.tabla_ordenes.delete(i)

        if self.cnx.is_connected():

            print(".....OBTENIENDO INFORMACIÓN DE LA ORDEN DE TRABAJO.....")

            cursor = self.cnx.cursor()

            # Parametros del proceso almacenado
            parametros = [self.buscar.get(),]

            # Llama al proceso almacenado
            cursor.callproc('spObtenerOrdenes', parametros)

            for result in cursor.stored_results():
                orden_obtenida = result.fetchall()
                print(orden_obtenida)

            i = 0
            total_pendientes = 0
            total_entregados = 0

            total_saldos = 0
            total_abonos = 0
            total_generado = 0

            total_efectivo = 0
            total_transferencias = 0

            # Agregar cada orden obtenida al treeview
            for orden in orden_obtenida:
                i += 1
                id_orden = orden[0]
                num_orden = orden[1]
                fecha_pedido = orden[2].strftime("%Y-%m-%d")
                fecha_entrega = orden[3].strftime("%Y-%m-%d")
                estado = orden[4]
                saldo = orden[5]
                total = orden[6]
                nombre_cliente = orden[7]
                cedula = orden[8]
                telefono = orden[9]
                email = orden[10]
                responsable = orden[11] + ' ' + orden[12]

                print('..... DETALLES DE LA ORDEN N°: ' + str(num_orden) + '......')
                print ('id_orden : ' + str(id_orden))
                print('fecha pedido : ' + fecha_pedido)
                print('fecha entrega : ' + fecha_entrega)
                print('Estado : ' + estado)
                print('Saldo:' + str(saldo))
                print('Total a pagar: ' + str(total))
                print('Cliente: ' + nombre_cliente)
                print('Cédula: ' + cedula)
                print('Teléfono: ' + telefono)
                print('Correo: ' + email)
                print('Responsable:' + responsable)

                total_saldos += saldo
                total_generado += total

                if estado == 'PENDIENTE':
                    total_pendientes += 1
                if estado == 'ENTREGADO':
                    total_entregados += 1

                detalle_orden = (i, num_orden, fecha_pedido, nombre_cliente, telefono, fecha_entrega, estado, saldo, total,  responsable )

                self.tabla_ordenes.insert("", 'end', iid=id_orden,
                                          values=detalle_orden)

            self.total_ordenes.set(i)
            self.total_pendientes.set(total_pendientes)
            self.total_entregadas.set(total_entregados)
            self.total_saldo.set(total_saldos)
            self.total_generado.set(total_generado)
            self.total_efectivo.set(total_efectivo)
            self.total_transferencias.set(total_transferencias)

            print('ORDENES GENERADAS: ' + str(self.total_ordenes))
            print('ORDENES PENDIENTES: ' + str(self.total_pendientes))
            print('ORDENES ENTREGADAS: ' + str(self.total_entregadas))


            self.cnx.commit()
        else:
            print("Connection failure")