from crud.book import create_book, read_all_books, update_book, delete_book
from utils.queries import read_query, delete_query
from utils.create_table import create_book_table_if_not_exists

def book_menu(connection):
    create_book_table_if_not_exists(connection)

    print("\nMenu de Livros:")
    print("1. Criar um novo livro")
    print("2. Ler todos os livros")
    print("3. Atualizar um livro")
    print("4. Deletar um livro")
    escolha = input("Digite o número da opção desejada: ")

    if escolha == '1':
        create_book(connection)
    elif escolha == '2':
        read_query(connection, "Livro")
    elif escolha == '3':
        update_book(connection)
    elif escolha == '4':
        delete_query(connection, "Livro")
    else:
        print("Opção inválida, tente novamente.")