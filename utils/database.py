import mysql.connector
from mysql.connector import Error

def connect():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='biblioteca',
            user='root',
            password='940860117'
        )
        if connection.is_connected():
            print("Conexão bem-sucedida!")
            return connection
    except Error as e:
        print("Erro ao conectar ao MySQL:", e)
        return None