import mysql.connector
from mysql.connector import Error
from utils.queries import create_query

# Funções CRUD para a entidade "Membro"
def create_member(connection):
    try:
        nome = input("Digite o nome do membro: ")
        sobrenome = input("Digite o sobrenome do membro: ")
        endereco = input("Digite o endereço do membro: ")
        email = input("Digite o email do membro: ")
        
        create_query(
            connection,
            "Emprestimo",
            "nome, sobrenome, endereco, email",
            [(nome, sobrenome, endereco, email)]
        )
        print("Membro criado com sucesso!")
    except Error as e:
        print("Erro ao criar o membro:", e)

def read_all_members(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Membro")
        members = cursor.fetchall()
        for member in members:
            print(member)
    except Error as e:
        print("Erro ao ler os membros:", e)

def update_member(connection):
    try:
        cursor = connection.cursor()
        membro_id = input("Digite o ID do membro que deseja atualizar: ")
        novo_email = input("Digite o novo email do membro: ")
        mysql_update_query = """UPDATE Membro SET email = %s WHERE id = %s"""
        cursor.execute(mysql_update_query, (novo_email, membro_id))
        connection.commit()
        print("Membro atualizado com sucesso!")
    except Error as e:
        print("Erro ao atualizar o membro:", e)

def delete_member(connection):
    try:
        cursor = connection.cursor()
        membro_id = input("Digite o ID do membro que deseja deletar: ")
        mysql_delete_query = """DELETE FROM Membro WHERE id = %s"""
        cursor.execute(mysql_delete_query, (membro_id,))
        connection.commit()
        print("Membro deletado com sucesso!")
    except Error as e:
        print("Erro ao deletar o membro:", e)