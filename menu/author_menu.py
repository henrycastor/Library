from crud.author import create_author, read_all_authors, update_author, delete_author
from utils.queries import read_query, delete_query
from utils.create_table import create_author_table_if_not_exists

def author_menu(connection):
    create_author_table_if_not_exists(connection)

    print("\nMenu de Autores:")
    print("1. Criar um novo autor")
    print("2. Ler todos os autores")
    print("3. Atualizar um autor")
    print("4. Deletar um autor")
    escolha = input("Digite o número da opção desejada: ")

    if escolha == '1':
        create_author(connection)
    elif escolha == '2':
        read_query(connection, "Autor")
    elif escolha == '3':
        update_author(connection)
    elif escolha == '4':
        delete_query(connection, "Autor")
    else:
        print("Opção inválida, tente novamente.")