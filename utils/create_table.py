import mysql.connector
from mysql.connector import Error
from utils.database import connect

# change file name because it also creates the database

# remember to create the function to create the database 'biblioteca'
# or to put it in the functions bellow
# or on connect function, preferably in the former

# remember to make all the functions above one that's generic

def create_database_if_not_exists():
    try:
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS biblioteca;")
        print("Banco de dados 'biblioteca' verificado/criado com sucesso.")
    except mysql.connector.Error as e:
        print("Erro ao criar/verificar o banco de dados:", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def create_book_table_if_not_exists(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS Livro (
            id INT AUTO_INCREMENT PRIMARY KEY,
            titulo VARCHAR(255) NOT NULL,
            autor_id INT NOT NULL,
            isbn VARCHAR(20),
            genero VARCHAR(100),
            ano_publicacao YEAR,
            FOREIGN KEY (autor_id) REFERENCES Autor(id)
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Tabela 'Livro' verificada/criada com sucesso.")
    except Error as e:
        print("Erro ao criar/verificar a tabela 'Livro':", e)

def create_author_table_if_not_exists(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS Autor (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            sobrenome VARCHAR(100) NOT NULL,
            nacionalidade VARCHAR(100)
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Tabela 'Autor' verificada/criada com sucesso.")
    except Error as e:
        print("Erro ao criar/verificar a tabela 'Autor':", e)

def create_member_table_if_not_exists(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS Membro (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            sobrenome VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE,
            telefone VARCHAR(15)
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Tabela 'Membro' verificada/criada com sucesso.")
    except Error as e:
        print("Erro ao criar/verificar a tabela 'Membro':", e)

def create_loan_table_if_not_exists(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS Emprestimo (
            id INT AUTO_INCREMENT PRIMARY KEY,
            livro_id INT NOT NULL,
            membro_id INT NOT NULL,
            data_emprestimo DATE NOT NULL,
            data_devolucao DATE,
            FOREIGN KEY (livro_id) REFERENCES Livro(id),
            FOREIGN KEY (membro_id) REFERENCES Membro(id)
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Tabela 'Emprestimo' verificada/criada com sucesso.")
    except Error as e:
        print("Erro ao criar/verificar a tabela 'Emprestimo':", e)