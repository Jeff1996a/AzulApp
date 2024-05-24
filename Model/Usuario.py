
class Usuario :

    def __init__(self, nombres, apellidos, username, password, rol, id_caja):

        self.nombres = nombres
        self.apellidos= apellidos
        self.username = username
        self.password = password
        self.rol = rol
        self.id_caja = id_caja

    def iniciar_sesion(self, username, password):
        pass

    def cerrar_sesion(self):
        pass


