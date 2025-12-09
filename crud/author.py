import mysql.connector
from mysql.connector import Error
from utils.create_table import create_author_table_if_not_exists
from utils.queries import create_query, read_query, update_query

def get_author_id(connection, nome, sobrenome):
    try:
        cursor = connection.cursor()
        query = "SELECT id FROM Autor WHERE nome = %s AND sobrenome = %s"
        cursor.execute(query, (nome, sobrenome))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    except Error as e:
        print("Erro ao buscar o autor:", e)
        return None
    
# Put together the functions to create an author

# Função para criar um autor
def create_author_direct(connection, nome, sobrenome, nacionalidade):
    try:
        create_author_table_if_not_exists(connection)
        cursor = connection.cursor()
        mysql_insert_query = """INSERT INTO Autor (nome, sobrenome, nacionalidade) 
                                VALUES (%s, %s, %s)"""
        record_to_insert = (nome, sobrenome, nacionalidade)
        cursor.execute(mysql_insert_query, record_to_insert)
        connection.commit()
        return cursor.lastrowid  # Retorna o ID do autor recém-criado
    except Error as e:
        print("Erro ao criar o autor:", e)
        return None

# Funções CRUD para a entidade "Autor"
def create_author(connection):
    try:
        nome = input("Digite o nome do autor: ")
        sobrenome = input("Digite o sobrenome do autor: ")
        nacionalidade = input("Digite a nacionalidade do autor: ")
        
        create_query(
            connection,
            "Autor",
            "nome, sobrenome, nacionalidade",
            [(nome, sobrenome, nacionalidade)]
        )
        print("Autor criado com sucesso!")
    except Error as e:
        print("Erro ao criar o autor:", e)

def read_all_authors(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Autor")
        authors = cursor.fetchall()
        for author in authors:
            print(author)
    except Error as e:
        print("Erro ao ler os autores:", e)

def update_author(connection, autor_id, novo_nome, novo_sobrenome):
    update_query(
        connection,
        "Autor",
        "autor_id, novo_nome, novo_sobrenome",
        [(autor_id, novo_nome, novo_sobrenome)]
    )

def update_author(connection):
    try:
        cursor = connection.cursor()
        autor_id = input("Digite o ID do autor que deseja atualizar: ")
        novo_nome = input("Digite o novo nome do autor: ")
        mysql_update_query = """UPDATE Autor SET nome = %s WHERE id = %s"""
        cursor.execute(mysql_update_query, (novo_nome, autor_id))
        connection.commit()
        print("Autor atualizado com sucesso!")
    except Error as e:
        print("Erro ao atualizar o autor:", e)

def delete_author(connection):
    try:
        cursor = connection.cursor()
        autor_id = input("Digite o ID do autor que deseja deletar: ")
        mysql_delete_query = """DELETE FROM Autor WHERE id = %s"""
        cursor.execute(mysql_delete_query, (autor_id,))
        connection.commit()
        print("Autor deletado com sucesso!")
    except Error as e:
        print("Erro ao deletar o autor:", e)