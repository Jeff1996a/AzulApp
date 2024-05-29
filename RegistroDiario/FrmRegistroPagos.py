import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
from tkcalendar import *
from datetime import date

from dbConnection import  dbConnection

class FrmRegistroPagos(tk.Toplevel):
    def __init__(self, datos_usuario):
        super().__init__()
        self.datos_usuario = datos_usuario

        # Conexión a la base de datos Azul lavandería
        self.db = dbConnection()
        self.cnx = self.db.cnx

        # ******************************************TITULO DEL FORMULARIO**********************************
        self.lblTitulo = ttk.Label(self, text='Azul Lavandería', font=('Courier', 20), foreground='blue')
        self.lblTitulo.pack(side='top', padx=20, pady=5)

        # Subtitulo del formulario
        self.label_subtitulo = ttk.Label(self, text='Registro diario de caja', font=('Courier', 15),
                                         foreground='purple')
        self.label_subtitulo.pack(side='top', anchor='center', padx=15, pady=5)

        # *****************************************CONTENEDOR PRINCIPAL**********************************************
        # Contenedor principal pagos
        self.contenedor_pagos = tk.LabelFrame(self, text='REGISTRO DE PAGOS INGRESADOS', font=("Courier", 12),
                                                  foreground='green')
        self.contenedor_pagos.pack(side='top', fill='both', padx=5, pady=5)

        # *****************************************CONTENEDOR BUSCAR PAGOS ***********************************************
        # Contenedor buscar ordenes por fecha
        self.contenedor_buscar = ttk.Frame(self.contenedor_pagos)
        self.contenedor_buscar.pack(side='top', fill='both', padx=0, pady=0)

        # Label para el contenedor buscar
        self.lbl_buscar = ttk.Label(self.contenedor_buscar, text='Fecha pedido:', font=('Courier', 10))
        self.lbl_buscar.pack(side='left', anchor='w', padx=0, pady=0, ipadx=0, ipady=2)

        # Entry para el contenedor buscar
        self.buscar = tk.StringVar()

        self.txt_buscar = ttk.Entry(self.contenedor_buscar, width=30)
        self.txt_buscar.pack(side='left', padx=2, pady=0)


        # Create an object of tkinter ImageTk
        self.readImg = Image.open("Img/search.png")
        self.newImg = self.readImg.resize((15, 15))
        self.img = ImageTk.PhotoImage(self.newImg)

        # Botón para guardar los datos
        self.buscar_button = ttk.Button(
            self.contenedor_buscar,
            image=self.img,
            command=self.obtener_pagos,
            compound='right',
            width=3,
        )
        self.buscar_button.pack(side='left', anchor='center', ipadx=2, ipady=0, padx=2)

        self.txt_buscar['textvariable'] = self.buscar

        # Calendario de fecha entrada
        self.contenedor_calendario = tk.Frame(self.contenedor_pagos)

        self.date_frame = tk.Frame(self.contenedor_calendario)
        self.date_frame.pack(side='left', fill='both')

        self.cal = Calendar(self.date_frame, selectmode='day', date_pattern='y-mm-dd')

        self.submit_date = ttk.Button(self.date_frame, text='INGRESAR', width=15, command=self.grab_date)
        self.txt_buscar.bind('<1>', self.pick_date)

        self.buscar.set(date.today().strftime("%Y-%m-%d"))

        # **********************************************CONTENEDOR TABLA INGRESOS**************************************
        self.contenedor_tabla = tk.Frame(self.contenedor_pagos)
        self.contenedor_tabla.pack(side='bottom', fill='both')

        # Contenedor principal
        self.contenedor_pagos = tk.LabelFrame(self, text='PAGOS INGRESADOS', font=("Courier", 12),
                                              foreground='green')
        self.contenedor_pagos.pack(side='top', fill='both', padx=5, pady=0)

        # Treeview para los productos del inventario
        self.encabezado = ('#1', '#2', '#3', '#4', '#5', '#6', '#7', '#8', '#9', '#10', '#11', '#12')
        self.tabla_pagos = ttk.Treeview(self.contenedor_tabla, columns=self.encabezado, show='headings', height=8)
        self.tabla_pagos.pack(side='bottom', fill='both', padx=5, pady=5)

        self.tabla_pagos.column('#1', width=25, minwidth=25, stretch=False, anchor='center')
        self.tabla_pagos.column('#2', width=80, minwidth=80, stretch=False, anchor='center')
        self.tabla_pagos.column('#3', width=120, minwidth=120, stretch=False, anchor='center')
        self.tabla_pagos.column('#4', width=220, minwidth=220, stretch=False, anchor='center')
        self.tabla_pagos.column('#5', width=120, minwidth=120, stretch=False, anchor='center')
        self.tabla_pagos.column('#6', width=120, minwidth=120, stretch=False, anchor='center')
        self.tabla_pagos.column('#7', width=100, minwidth=100, stretch=False, anchor='center')
        self.tabla_pagos.column('#8', width=100, minwidth=100, stretch=False, anchor='center')
        self.tabla_pagos.column('#9', width=100, minwidth=100, stretch=False, anchor='center')
        self.tabla_pagos.column('#10', width=120, minwidth=120, stretch=False, anchor='center')
        self.tabla_pagos.column('#11', width=120, minwidth=120, stretch=False, anchor='center')

        self.tabla_pagos.heading('#1', text="N° PAGO", anchor='center')
        self.tabla_pagos.heading('#2', text='NUM. ORDEN', anchor='center')
        self.tabla_pagos.heading('#3', text='FECHA PEDIDO', anchor='center')
        self.tabla_pagos.heading('#4', text='CLIENTE')
        self.tabla_pagos.heading('#5', text='FECHA ENTREGA', anchor='center')
        self.tabla_pagos.heading('#6', text='ESTADO', anchor='center')
        self.tabla_pagos.heading('#7', text='SALDO ($)', anchor='center')
        self.tabla_pagos.heading('#8', text='IMPORTE ($)', anchor='center')
        self.tabla_pagos.heading('#9', text='TOTAL ($)', anchor='center')
        self.tabla_pagos.heading('#10', text='TIPO DE PAGO', anchor='center')
        self.tabla_pagos.heading('#11', text='RESPONSABLE', anchor='center')

        # **********************************************CONTENEDOR TABLA GASTOS**************************************

        # Contenedor principal
        self.contenedor_gastos = tk.LabelFrame(self, text='REGISTRO DE GASTOS', font=("Courier", 12),
                                              foreground='green')
        self.contenedor_gastos.pack(side='top', fill='both', padx=5, pady=0)


        # Treeview para los productos del inventario
        self.encabezado2 = ('#1', '#2', '#3', '#4')
        self.tabla_gastos = ttk.Treeview(self.contenedor_gastos, columns=self.encabezado2, show='headings', height=3)
        self.tabla_gastos.pack(side='left', padx=5, pady=5)

        self.tabla_gastos.column('#1', width=25, minwidth=25, stretch=False, anchor='center')
        self.tabla_gastos.column('#2', width=180, minwidth=128, stretch=False, anchor='center')
        self.tabla_gastos.column('#3', width=80, minwidth=80, stretch=False, anchor='center')
        self.tabla_gastos.column('#4', width=120, minwidth=120, stretch=False, anchor='center')

        self.tabla_gastos.heading('#1', text="N° GASTO", anchor='center')
        self.tabla_gastos.heading('#2', text='DESCRIPCIÓN', anchor='center')
        self.tabla_gastos.heading('#3', text='TOTAL ($)', anchor='center')
        self.tabla_gastos.heading('#4', text='RESPONSABLE', anchor='center')

        # *******************************************CONTENEDOR RESUMEN CAJA**************************************
        # Contenedor resumen caja
        self.contenedor_resumen_pagos= tk.Frame(self)
        self.contenedor_resumen_pagos.pack(side='top', fill='both', padx=0, pady=5)

        # ******CONTENEDOR INGRESOS**********
        self.contenedor_ingresos = tk.LabelFrame(self.contenedor_resumen_pagos, text='RESUMEN DIARIO', font=("Courier", 12), foreground='green')
        self.contenedor_ingresos.pack(side='left', padx=5, pady=3, ipadx=15, ipady=3)

        self.total_importes = tk.DoubleVar()

        # Contenedor resumen importes generados
        self.contenedor_importes = tk.Frame(self.contenedor_ingresos)
        self.contenedor_importes.pack(side='top')

        # Label total importes
        self.label_total_importes = ttk.Label(self.contenedor_importes, text='Importe diario ($):',  font=("Courier", 10),
                                              width=22)
        self.label_total_importes.pack(side='left', anchor='w', padx=0, pady=0)

        # Entry total importes
        self.txt_total_importes = ttk.Button(self.contenedor_importes,width=15, textvariable=self.total_importes)
        self.txt_total_importes.pack(side='left', anchor='w', padx=0, pady=0)

        # ******************************************************* TOTAL SALDOS PENDIENTES********************************

        self.total_saldos = tk.DoubleVar()

        # Contenedor resumen saldos pendientes
        self.contenedor_saldos = tk.Frame(self.contenedor_ingresos)
        self.contenedor_saldos.pack(side='top')

        # Label total saldos
        self.label_total_saldos = ttk.Label(self.contenedor_saldos, text='Saldos pendientes ($):',
                                              font=("Courier", 10), width=22)
        self.label_total_saldos.pack(side='left', anchor='w', padx=0, pady=0)

        # Entry total saldos
        self.txt_total_saldos = ttk.Button(self.contenedor_saldos, width=15, textvariable=self.total_saldos)
        self.txt_total_saldos.pack(side='left', anchor='w', padx=0, pady=0)

        # ******CONTENEDOR METODOS DE PAGO**********
        self.contenedor_metodos = tk.LabelFrame(self.contenedor_resumen_pagos, text='MÉTODOS DE PAGO', font=("Courier", 12), foreground='green')
        self.contenedor_metodos.pack(side='left', padx=5, pady=0, ipadx=15, ipady=3)

        self.total_efectivo = tk.DoubleVar()

        # Contenedor total efectivo
        self.contenedor_efectivo = tk.Frame(self.contenedor_metodos)
        self.contenedor_efectivo.pack(side='top')

        # Label total efectivo
        self.label_total_efectivo = ttk.Label(self.contenedor_efectivo, text='Total efectivo ($):',
                                              font=("Courier", 10),
                                              width=25)
        self.label_total_efectivo.pack(side='left', anchor='w', padx=0, pady=0)

        # Entry total efectivo
        self.txt_total_efectivo = ttk.Button(self.contenedor_efectivo, width=15, textvariable=self.total_efectivo)
        self.txt_total_efectivo.pack(side='left', anchor='w', padx=0, pady=0)

        self.total_transferencias = tk.DoubleVar()

        # Contenedor total transferencias
        self.contenedor_transferencias = tk.Frame(self.contenedor_metodos)
        self.contenedor_transferencias.pack(side='top')

        # Label total transferencias
        self.label_total_transferencias = ttk.Label(self.contenedor_transferencias, text='Total transferencias ($):',
                                              font=("Courier", 10),
                                              width=25)
        self.label_total_transferencias.pack(side='left', anchor='w', padx=0, pady=0)

        # Entry total transferencias
        self.txt_total_transferencias = ttk.Button(self.contenedor_transferencias, width=15, textvariable=self.total_transferencias)
        self.txt_total_transferencias.pack(side='left', anchor='w', padx=0, pady=0)

        # ******CONTENEDOR TOTALES**********
        self.contenedor_totales = tk.LabelFrame(self.contenedor_resumen_pagos, text='RESUMEN TOTAL',
                                                font=("Courier", 12), foreground='green')
        self.contenedor_totales.pack(side='left', padx=5, pady=0, ipadx=15, ipady=3)

        self.total_ingresos = tk.DoubleVar()

        # Contenedor total ingresos
        self.contenedor_ingresos = tk.Frame(self.contenedor_totales)
        self.contenedor_ingresos.pack(side='top')

        # Label total ingresos
        self.label_total_ingresos = ttk.Label(self.contenedor_ingresos, text='TOTAL INGRESOS ($):',
                                              font=("Courier", 10),
                                              width=25)
        self.label_total_ingresos.pack(side='left', anchor='w', padx=0, pady=0)

        # Entry total ingresos
        self.txt_total_ingresos = ttk.Button(self.contenedor_ingresos, width=15, textvariable=self.total_ingresos)
        self.txt_total_ingresos.pack(side='left', anchor='w', padx=0, pady=0)

        self.total_egresos = tk.DoubleVar()

        # Contenedor total egresos
        self.contenedor_egresos = tk.Frame(self.contenedor_totales)
        self.contenedor_egresos.pack(side='top')

        # Label total egresos
        self.label_total_egresos = ttk.Label(self.contenedor_egresos, text='TOTAL GASTOS ($):',
                                                    font=("Courier", 10),
                                                    width=25)
        self.label_total_egresos.pack(side='left', anchor='w', padx=0, pady=0)

        # Entry total egresos
        self.txt_total_egresos = ttk.Button(self.contenedor_egresos, width=15, textvariable=self.total_egresos)
        self.txt_total_egresos.pack(side='left', anchor='w', padx=0, pady=0)

        # ******CONTENEDOR SALDO CAJA**********
        self.contenedor_caja= tk.LabelFrame(self.contenedor_resumen_pagos, text='SALDO TOTAL',
                                                font=("Courier", 12), foreground='green')
        self.contenedor_caja.pack(side='left', padx=5, pady=0, ipadx=15, ipady=3)

        self.total_caja = tk.StringVar()

        # Contenedor total ingresos
        self.contenedor_saldo_caja = tk.Frame(self.contenedor_caja)
        self.contenedor_saldo_caja.pack(side='top')

        # Label total ingresos
        self.label_calculo = ttk.Label(self.contenedor_saldo_caja, text='Ingresos-Gastos',
                                              font=("Courier", 10),
                                              width=25, foreground='gray')
        self.label_calculo.pack(side='top', anchor='center', padx=0, pady=0)

        self.label_saldo_caja = ttk.Label(self.contenedor_saldo_caja, text='', textvariable=self.total_caja,
                                       font=("Courier", 16),
                                       width=25, foreground='gray')
        self.label_saldo_caja.pack(side='top', anchor='center', padx=0, pady=0)

        self.total_caja.set('0.00 $')

        self.obtener_pagos()

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

    def obtener_pagos(self):
        pagos_realizados = []

        total_pendientes = 0
        total_importes = 0
        total_efectivo = 0
        total_transferencias = 0

        total_caja = 0

        # Limpiar la tabla
        for i in self.tabla_pagos.get_children():
            self.tabla_pagos.delete(i)

        if self.cnx.is_connected():

            print(".....OBTENIENDO INFORMACIÓN DE PAGOS INGRESADOS EN CAJA.....")

            cursor = self.cnx.cursor()

            # Parametros del proceso almacenado
            parametros = [self.buscar.get(), ]

            # Llama al proceso almacenado
            cursor.callproc('spObtenerPagos', parametros)

            for result in cursor.stored_results():
                pagos_realizados = result.fetchall()
                print(pagos_realizados)

            i = 0

            for pago in pagos_realizados:
                print(pago)

                estado_orden = pago[5]
                tipo_pago = pago[9]

                if tipo_pago == 'EFECTIVO':
                    total_efectivo += pago[7]
                if tipo_pago == 'TRANSFERENCIA':
                    total_transferencias += pago[7]

                total_importes += pago[7]

                if estado_orden == "PENDIENTE":
                    total_pendientes += pago[6]

                self.tabla_pagos.insert("", 'end', iid=i, values=pago)

                i += 1

            self.total_importes.set(round(total_importes, 2))
            self.total_ingresos.set(round(total_importes, 2))
            self.total_saldos.set(round(total_pendientes, 2))
            self.total_efectivo.set(round(total_efectivo, 2))
            self.total_transferencias.set(round(total_transferencias, 2))

            self.cnx.commit()

            self.obtener_gastos()

            total_caja = round(self.total_ingresos.get() - self.total_egresos.get(), 2)

            self.total_caja.set(str(total_caja) + ' $')
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

    def obtener_gastos(self):

        # Limpiar la tabla
        for i in self.tabla_gastos.get_children():
            self.tabla_gastos.delete(i)

        gastos_obtenidos = []

        total_gastos = 0

        if self.cnx.is_connected():
            print(".....INGRESANDO NUEVO GASTO.....")
            cursor = self.cnx.cursor()

            # To pass the input Arguments create a client
            parametro = [self.buscar.get()]
            cursor.callproc('spObtenerGastos', parametro)

            for result in cursor.stored_results():
                gastos_obtenidos = result.fetchall()
                print(gastos_obtenidos)

            i = 0
            for gasto in gastos_obtenidos:
                nuevo_gasto = (gasto[0], gasto[2], gasto[3], gasto[5])

                total_gastos += gasto[3]

                self.tabla_gastos.insert("", 'end', iid=i, values=nuevo_gasto)
                i += 1

            # Imprimir la última fila agregada
            self.cnx.commit()

            self.total_egresos.set(total_gastos)

        else:
            print("Connection failure")