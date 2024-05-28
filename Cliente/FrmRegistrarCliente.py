import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image

from dbConnection import dbConnection


class RegistrarCliente(tk.Toplevel):

    def __init__(self, datos_usuario):

        super().__init__()

        self.datos_usuario = datos_usuario

        self.lblTitulo = ttk.Label(self, text='Azul Lavandería', font=('Courier', 20), foreground='blue')
        self.lblTitulo.pack(side='top', padx=20, pady=5)

        # Pregunta de bienvenida
        self.lblQuestion = ttk.Label(self, text='Registrar nuevo cliente ', font=('Courier', 15), foreground='purple')
        self.lblQuestion.pack(side='top', anchor='center', padx=15, pady=5)

        # Contenedor datos cliente
        self.frm_crear_cliente = tk.LabelFrame(self, text='DATOS DEL CLIENTE', font=("Courier", 12),
                                              foreground='green')
        self.frm_crear_cliente.pack(side='top', fill='both', padx=10, pady=5)

        # Contenedor para la cédula del cliente
        self.cedula_container = tk.Frame(self.frm_crear_cliente)
        self.cedula_container.pack(side="top")

        # Label cédula del cliente
        self.lblcedula = ttk.Label(self.cedula_container, text='CÉDULA/PASAPORTE:', font=("Courier", 10), width=20)
        self.lblcedula.pack(side='left', anchor='nw', padx=5, pady=4, ipadx=4, ipady=4)

        # Text cédula del cliente
        self.txtCedula = ttk.Entry(self.cedula_container, width=30)
        self.txtCedula.pack(padx=8, pady=5, ipadx=4, ipady=4)
        self.txtCedula.focus_set()

        # Contenedor para los nombres del cliente
        self.nombres_container = tk.Frame(self.frm_crear_cliente)
        self.nombres_container.pack(side="top")

        # Label nombres del cliente
        self.lblname = ttk.Label(self.nombres_container, text='APELLIDOS Y NOMBRES:', font=("Courier", 10), width=20)
        self.lblname.pack(side='left', anchor='nw', padx=5, pady=4, ipadx=4, ipady=4)

        # Text nombres del cliente
        self.txtnombre = ttk.Entry(self.nombres_container, width=30)
        self.txtnombre.pack(padx=8, pady=5, ipadx=4, ipady=4)

        # Contenedor para la dirección del cliente
        self.direccion_container = tk.Frame(self.frm_crear_cliente)
        self.direccion_container.pack(side="top")

        # Label direccion del cliente
        self.lbldireccion = ttk.Label(self.direccion_container, text='DIRECCIÓN:', font=("Courier", 10), width=20)
        self.lbldireccion.pack(side='left', anchor='nw', padx=5, pady=4, ipadx=4, ipady=4)

        # Text direccion del cliente
        self.txtDireccion = ttk.Entry(self.direccion_container, width=30)
        self.txtDireccion.pack(padx=8, pady=5, ipadx=4, ipady=4)

        # Contenedor teléfono del cliente
        self.telefono_container = tk.Frame(self.frm_crear_cliente)
        self.telefono_container.pack(side="top")

        # Label telefono del cliente
        self.lblTelefono = ttk.Label(self.telefono_container, text='TELÉFONO:', font=("Courier", 10), width=20)
        self.lblTelefono.pack(side='left', anchor='nw', padx=5, pady=4, ipadx=4, ipady=4)

        # Text telefono del cliente
        self.txtTelefono = ttk.Entry(self.telefono_container, width=30)
        self.txtTelefono.pack(padx=8, pady=5, ipadx=4, ipady=4)

        # Contenedor email del cliente
        self.email_container = tk.Frame(self.frm_crear_cliente)
        self.email_container.pack(side="top")

        # Label telefono del cliente
        self.lblEmail = ttk.Label(self.email_container, text='CORREO ELECTRÓNICO:', font=("Courier", 10), width=20)
        self.lblEmail.pack(side='left', anchor='nw', padx=5, pady=4, ipadx=4, ipady=4)

        # Text telefono del cliente
        self.txtEmail = ttk.Entry(self.email_container, width=30)
        self.txtEmail.pack(padx=8, pady=5, ipadx=4, ipady=4)

        # Contenedor para los botones
        self.button_container = tk.Frame(self)
        self.button_container.pack(side="bottom")
        # Create an object of tkinter ImageTk
        self.saveImg = Image.open("Img/save.png")
        self.newSaveImg = self.saveImg.resize((15, 15))
        self.save = ImageTk.PhotoImage(self.newSaveImg)

        # Botón para guardar los datos
        self.guardar_button = ttk.Button(
            self.button_container,
            text="GUARDAR",
            image=self.save,
            compound='right',
        )
        self.guardar_button.pack(side='left',anchor='center', padx=10, pady=10, ipadx=5, ipady=2)

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

        self.cedula = tk.StringVar()
        self.nombres = tk.StringVar()
        self.direccion = tk.StringVar()
        self.telefono = tk.StringVar()
        self.email = tk.StringVar()

        self.txtCedula['textvariable'] = self.cedula
        self.txtnombre['textvariable'] = self.nombres
        self.txtDireccion['textvariable'] = self.direccion
        self.txtTelefono['textvariable'] = self.telefono
        self.txtEmail['textvariable'] = self.email

        self.guardar_button.bind('<Button>', self.save_client)

        self.nombres.trace('w', self.upper_nombres)
        self.direccion.trace('w', self.upper_direccion)

        self.focus()

        self.grab_set()

    def save_client(self, event):

        # Conexión a la base de datos Azul lavandería
        db = dbConnection()

        cnx = db.cnx

        if (cnx.is_connected()):
            print("Esperando para enviar datos")
            cursor = cnx.cursor()

            # To pass the input Arguments create a client
            self.client_data = [self.nombres.get(), self.direccion.get(), self.telefono.get(), self.email.get(),
                                self.cedula.get()]
            cursor.callproc('spRegistrarCliente', self.client_data)

            result = 0

            for result in cursor.stored_results():
                a = result.fetchall()
                result = a[0]

            # Imprimir la última fila agregada
            id_cliente = result[0]

            # Ejecutar el proceso almacenadoe
            cnx.commit()

            if id_cliente == 0:
                messagebox.showerror(message='Cliente se encuentra registrado',
                                     title='Error de registro')
            else:
                messagebox.showinfo(message='Cliente registrado exitosamente',
                                    title='Registro completo')
                self.destroy()

            cursor.close()
            cnx.close()

        else:
            print("Connection failure")


    def upper_nombres(self, *args):
        self.nombres.set(self.nombres.get().upper())  # change to Upper case

    def upper_direccion(self, *args):
        self.direccion.set(self.direccion.get().upper())  # change to Upper case
