import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
from tkcalendar import *
from datetime import date

from dbConnection import  dbConnection

class FrmRegistroGastos(tk.Toplevel):
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
        self.label_subtitulo = ttk.Label(self, text='Control diario de gastos', font=('Courier', 15),
                                         foreground='purple')
        self.label_subtitulo.pack(side='top', anchor='center', padx=15, pady=5)

        # +**************** CONTENEDOR PRINCIPAL *******************+
        self.contenedor_nuevo_gasto = tk.LabelFrame(self, text='REGISTRO DE GASTOS', font=("Courier", 12),
                                                  foreground='green')
        self.contenedor_nuevo_gasto.pack(side='top', fill='both', padx=5, pady=0)

        # ***** DETALLE / DESCRIPCIÓN DE GASTO ******
        self.descripcion = tk.StringVar()  # Variable para obtener la fecha

        self.label_descripcion = ttk.Label(self.contenedor_nuevo_gasto, text='Descripción: ', font=('Courier', 10), width=15)
        self.label_descripcion.grid(sticky='nw', row=0, column=0, padx=5, pady=3)

        self.txt_descripcion = ttk.Entry(self.contenedor_nuevo_gasto, width=30, textvariable=self.descripcion)
        self.txt_descripcion.grid(sticky='nw', row=0, column=1, padx=5, pady=3)

        # Create an object of tkinter ImageTk
        self.addImg = Image.open("Img/add.png")
        self.newAddImg = self.addImg.resize((15, 15))
        self.add = ImageTk.PhotoImage(self.newAddImg)

        # Botón para agregar prendas
        self.btn_agregar_gasto = ttk.Button(
            self.contenedor_nuevo_gasto,
            text="AGREGAR",
            image=self.add,
            compound='right',
            command=self.registrar_gasto
        )
        self.btn_agregar_gasto.grid(row=0, column=2, padx=20, pady=0)

        # ***** TOTAL GASTO ******
        self.total = tk.DoubleVar()  # Variable para obtener la fecha

        self.label_total = ttk.Label(self.contenedor_nuevo_gasto, text='Total ($): ', font=('Courier', 10), width=10)
        self.label_total.grid(sticky='nw', row=1, column=0, padx=5, pady=3)

        self.txt_total = ttk.Entry(self.contenedor_nuevo_gasto, width=15, textvariable=self.total)
        self.txt_total.grid(sticky='nw', row=1, column=1, padx=5, pady=3)

        # +*************** CONTENEDOR TABLA GASTOS ***************+

        # Contenedor principal
        self.contenedor_gastos = tk.LabelFrame(self, text='GASTOS INGRESADOS', font=("Courier", 12),
                                              foreground='green')
        self.contenedor_gastos.pack(side='top', fill='both', padx=5, pady=5)

        # Contenedor buscar ordenes por fecha
        self.contenedor_buscar = ttk.Frame(self.contenedor_gastos)
        self.contenedor_buscar.pack(side='top', fill='both', padx=0, pady=0)

        # Label para el contenedor buscar
        self.lbl_buscar = ttk.Label(self.contenedor_buscar, text='Fecha de ingreso:', font=('Courier', 10))
        self.lbl_buscar.pack(side='left', anchor='w', padx=0, pady=0, ipadx=0, ipady=2)

        # Entry para el contenedor buscar
        self.buscar = tk.StringVar()

        self.txt_buscar = ttk.Entry(self.contenedor_buscar, width=20)
        self.txt_buscar.pack(side='left', padx=2, pady=0)

        # Create an object of tkinter ImageTk
        self.readImg = Image.open("Img/search.png")
        self.newImg = self.readImg.resize((15, 15))
        self.img = ImageTk.PhotoImage(self.newImg)

        # Botón para guardar los datos
        self.buscar_button = ttk.Button(
            self.contenedor_buscar,
            image=self.img,
            command=self.destroy,
            compound='right',
            width=3,
        )
        self.buscar_button.pack(side='left', anchor='center', ipadx=0, ipady=0, padx=2)

        self.txt_buscar['textvariable'] = self.buscar

        # Calendario de fecha entrada
        self.contenedor_calendario = tk.Frame(self.contenedor_gastos)

        self.date_frame = tk.Frame(self.contenedor_calendario)
        self.date_frame.pack(side='left', fill='both')

        self.cal = Calendar(self.date_frame, selectmode='day', date_pattern='y-mm-dd')

        self.submit_date = ttk.Button(self.date_frame, text='INGRESAR', width=15, command=self.grab_date)
        self.txt_buscar.bind('<1>', self.pick_date)

        self.buscar.set(date.today().strftime("%Y-%m-%d"))

        # Treeview para los productos del inventario
        self.encabezado = ('#1', '#2', '#3')
        self.tabla_gastos = ttk.Treeview(self.contenedor_gastos, columns=self.encabezado, show='headings', height=6)
        self.tabla_gastos.pack(side='bottom', anchor='w', padx=5, pady=5)

        self.tabla_gastos.column('#1', width=25, minwidth=25, stretch=False, anchor='center')
        self.tabla_gastos.column('#2', width=200, minwidth=200, stretch=False, anchor='center')
        self.tabla_gastos.column('#3', width=80, minwidth=80, stretch=False, anchor='center')

        self.tabla_gastos.heading('#1', text="N° GASTO", anchor='center')
        self.tabla_gastos.heading('#2', text='DESCRIPCIÓN / DETALLE', anchor='center')
        self.tabla_gastos.heading('#3', text='TOTAL ($)', anchor='center')

        self.obtener_gastos()

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

    def registrar_gasto(self):
        if self.cnx.is_connected():
            print(".....INGRESANDO NUEVO GASTO.....")
            cursor = self.cnx.cursor()

            # To pass the input Arguments create a client
            datos_gasto = [datetime.datetime.now(), self.descripcion.get(), self.total.get(), self.datos_usuario.id,
                           self.datos_usuario.id_caja]
            cursor.callproc('spRegistrarGasto', datos_gasto)

            response = []

            for result in cursor.stored_results():
                response = result.fetchall()

            # Imprimir la última fila agregada
            self.cnx.commit()

            id_gasto = response[0][0]
            print('El id gasto: ' + str(id_gasto))

            if id_gasto == 0:
                messagebox.showerror(message='NO SE PUDO REGISTRAR EL GASTO!!',
                                     title='Error de registro')
            else:
                self.obtener_gastos()
                messagebox.showinfo(message='SE HA REGISTRADO EXITOSAMENTE!!',
                                    title='Registro completo')
                self.destroy()

        else:
            print("Connection failure")

    def obtener_gastos(self):

        # Limpiar la tabla
        for i in self.tabla_gastos.get_children():
            self.tabla_gastos.delete(i)

        gastos_obtenidos = []

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
                nuevo_gasto = (gasto[0], gasto[2], gasto[3])
                self.tabla_gastos.insert("", 'end', iid=i, values=nuevo_gasto)
                i += 1

            # Imprimir la última fila agregada
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