import tkinter as tk

from Model.Usuario import Usuario
from dbConnection import dbConnection
from menu import MenuPrincipal
from tkinter import ttk
from PIL import ImageTk, Image
from datetime import date, datetime

class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.pack(side='top')

        # Definir un Frame para mostrar la imagen de bienvenida
        self.frame = ttk.Frame(self)
        self.frame.pack(padx=0, pady=10)

        # Create an object of tkinter ImageTk
        self.readImg = Image.open("Img/AzulLavanderia.png")
        self.newImg = self.readImg.resize((350, 250))
        self.img = ImageTk.PhotoImage(self.newImg)

        # Create a Label Widget to display the text or Image
        self.label = ttk.Label(self.frame, image=self.img)
        self.label.pack()

        # Label username
        self.lblUsername = ttk.Label(text='Usuario:', font=("Courier", 10))
        self.lblUsername.pack()

        # Text username
        self.txtUsername = ttk.Entry( width=25)
        self.txtUsername.pack(padx=0, pady=5, ipadx=4, ipady=4)
        self.txtUsername.focus()

        # Label password
        self.lblPassword = tk.Label(text='Contraseña:', font=("Courier",10))
        self.lblPassword.pack()

        # Text username
        self.txtPassword = ttk.Entry(show='*', width=25)
        self.txtPassword.pack(ipadx=4, ipady=4)

        # Label password
        self.lblAlerta = tk.Label(text='', font=("Courier", 8), foreground='red')
        self.lblAlerta.pack()


        # Create the application variable.
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.alerta = tk.StringVar()

        # Tell the entry widget to watch this variable.
        self.txtUsername["textvariable"] = self.username
        self.txtPassword["textvariable"] = self.password
        self.lblAlerta["textvariable"] = self.alerta

        # Define a callback for when the user hits return.
        self.btnLogin = ttk.Button(text='INGRESAR' )
        self.btnLogin.pack(padx=0, pady=20, ipadx=5, ipady=5)

        self.btnLogin.bind('<Button>', self.login)

    def login(self, event):

        # Conexión a la base de datos Azul lavandería
        db = dbConnection()

        cnx = db.cnx

        self.user_data = []

        if (cnx.is_connected):
            print("server connected")
            cursor = cnx.cursor()

            # To pass the input Arguments create a list and pass it
            args = [self.username.get(), self.password.get(),]
            cursor.callproc('spValidarUsuario', args)

            for result in cursor.stored_results():
                self.user_data = result.fetchall()

            datos_usuario = Usuario('', '', self.username.get(), self.password.get(), '', 0)

            try:
                datos_usuario.rol = self.user_data[0][0]
                datos_usuario.nombres = self.user_data[0][1]
                datos_usuario.apellidos = self.user_data[0][2]
                datos_usuario.id = self.user_data[0][3]

                if datos_usuario.rol == "admin":

                    now = datetime.now()

                    fecha_actual = now.strftime("%Y-%m-%d")
                    hora_apertura = now.strftime("%H:%M:%S")

                    print("HORA APERTURA: ", hora_apertura)
                    print("FECHA_CIERRE: ", fecha_actual)

                    print(".....REGISTRANDO APERTURA DE CAJA.......")

                    # To pass the input Arguments create a list and pass it
                    args = [datos_usuario.id, now]
                    cursor.callproc('spRegistrarAperturaCaja', args)

                    response = []

                    for result in cursor.stored_results():
                        response = result.fetchall()

                    cnx.commit()

                    datos_usuario.id_caja = response[0][0]
                    print('El número de caja asignado es: ' + str(datos_usuario.id_caja))

                    # Create secondary (or popup) window.
                    window = MenuPrincipal(datos_usuario)
                    self.master.withdraw()
                    self.txtUsername.focus()
                    self.username.set('')
                    self.password.set('')
                    self.alerta.set('')

                else:
                    self.alerta.set('Usuario o contraseña inconrrecta')
                    print("Usuario o contraseña incorrecta")
                    print("Usuario o contraseña incorrecta")
            except IndexError:
                self.alerta.set('Usuario o contraseña inconrrecta')
                print("Usuario o contraseña incorrecta")
        else:
            print("Connection failure")

root = tk.Tk()
myapp = App(root)
myapp.master.title('Azul Lavandería')
myapp.master.minsize(380,300)
myapp.master.anchor('n')
myapp.master.mainloop()



