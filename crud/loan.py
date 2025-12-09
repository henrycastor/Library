# Funções CRUD para a entidade "Empréstimo"
import mysql.connector
from mysql.connector import Error
from utils.queries import create_query

def create_loan(connection):
    try:
        livro_id = input("Digite o ID do livro: ")
        membro_id = input("Digite o ID do membro: ")
        data_emprestimo = input("Digite a data de empréstimo (YYYY-MM-DD): ")
        data_devolucao = input("Digite a data de devolução (YYYY-MM-DD): ")
        status = input("Digite o status do empréstimo: ")
        
        create_query(
            connection,
            "Emprestimo",
            "livro_id, membro_id, data_emprestimo, data_devolucao, status",
            [(livro_id, membro_id, data_emprestimo, data_devolucao, status)]
        )
        print("Empréstimo criado com sucesso!")
    except Error as e:
        print("Erro ao criar o empréstimo:", e)

def read_all_loans(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Emprestimo")
        loans = cursor.fetchall()
        for loan in loans:
            print(loan)
    except Error as e:
        print("Erro ao ler os empréstimos:", e)

def update_loan(connection):
    try:
        cursor = connection.cursor()
        emprestimo_id = input("Digite o ID do empréstimo que deseja atualizar: ")
        novo_status = input("Digite o novo status do empréstimo: ")
        mysql_update_query = """UPDATE Emprestimo SET status = %s WHERE id = %s"""
        cursor.execute(mysql_update_query, (novo_status, emprestimo_id))
        connection.commit()
        print("Empréstimo atualizado com sucesso!")
    except Error as e:
        print("Erro ao atualizar o empréstimo:", e)

def delete_loan(connection):
    try:
        cursor = connection.cursor()
        emprestimo_id = input("Digite o ID do empréstimo que deseja deletar: ")
        mysql_delete_query = """DELETE FROM Emprestimo WHERE id = %s"""
        cursor.execute(mysql_delete_query, (emprestimo_id,))
        connection.commit()
        print("Empréstimo deletado com sucesso!")
    except Error as e:
        print("Erro ao deletar o empréstimo:", e)