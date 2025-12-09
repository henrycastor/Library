import mysql.connector
from mysql.connector import Error
from crud.author import get_author_id, create_author, create_author_direct
from utils.database import connect
from utils.queries import create_query

# Funções CRUD para a entidade "Livro"
def create_book(connection):
    try:
        cursor = connection.cursor()
        titulo = input("Digite o título do livro: ")
        nome_autor = input("Digite o nome do autor: ")
        sobrenome_autor = input("Digite o sobrenome do autor: ")
        autor_id = get_author_id(connection, nome_autor, sobrenome_autor)
        
        if not autor_id:
            print(f"Autor '{nome_autor} {sobrenome_autor}' não encontrado.")
            nacionalidade = input("Digite a nacionalidade do autor: ")
            autor_id = create_author_direct(connection, nome_autor, sobrenome_autor, nacionalidade)
            if not autor_id:
                print("Criação de livro abortada.")
                return
        
        isbn = input("Digite o ISBN do livro: ")
        genero = input("Digite o gênero do livro: ")
        ano_publicacao = input("Digite o ano de publicação do livro: ")
        
        # Substituindo a consulta SQL direta pela função create_query
        create_query(
            connection,
            "Livro",
            "titulo, autor_id, isbn, genero, ano_publicacao",
            [(titulo, autor_id, isbn, genero, ano_publicacao)]
        )
        print("Livro criado com sucesso!")
    except Error as e:
        print("Erro ao criar o livro:", e)

def read_all_books(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT Livro.id, Livro.titulo, Autor.nome, Autor.sobrenome, Livro.isbn, Livro.genero, Livro.ano_publicacao
            FROM Livro
            JOIN Autor ON Livro.autor_id = Autor.id
        """)
        books = cursor.fetchall()
        for book in books:
            print(book)
    except Error as e:
        print("Erro ao ler os livros:", e)

def update_book(connection):
    try:
        cursor = connection.cursor()
        livro_id = input("Digite o ID do livro que deseja atualizar: ")
        novo_titulo = input("Digite o novo título do livro: ")
        
        mysql_update_query = """UPDATE Livro SET titulo = %s WHERE id = %s"""
        cursor.execute(mysql_update_query, (novo_titulo, livro_id))
        connection.commit()
        print("Livro atualizado com sucesso!")
    except Error as e:
        print("Erro ao atualizar o livro:", e)

def delete_book(connection):
    try:
        cursor = connection.cursor()
        livro_id = input("Digite o ID do livro que deseja deletar: ")
        mysql_delete_query = """DELETE FROM Livro WHERE id = %s"""
        cursor.execute(mysql_delete_query, (livro_id,))
        connection.commit()
        print("Livro deletado com sucesso!")
    except Error as e:
        print("Erro ao deletar o livro:", e)