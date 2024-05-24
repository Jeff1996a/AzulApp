import mysql.connector
from mysql.connector import errorcode

class dbConnection:

    def __init__(self):
        # Conexión a la base de datos Azul Lavandería
        try:
            self.cnx = mysql.connector.connect(user='ticscode', password='ticscode1996.',
                                          host='localhost',
                                          database='azuldb')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)