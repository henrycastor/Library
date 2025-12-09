from menu.book_menu import book_menu
from menu.author_menu import author_menu
from menu.member_menu import member_menu
from menu.loan_menu import loan_menu
from utils.database import connect
from utils.create_table import create_database_if_not_exists

def main():
    connection = connect()
    create_database_if_not_exists()
    if not connection:
        return

    while True:
        print("\nMenu Principal:")
        print("1. Menu de Livros")
        print("2. Menu de Autores")
        print("3. Menu de Membros")
        print("4. Menu de Empréstimos")
        print("5. Sair")
        escolha = input("Digite o número da opção desejada: ")

        if escolha == '1':
            book_menu(connection)
        elif escolha == '2':
            author_menu(connection)
        elif escolha == '3':
            member_menu(connection)
        elif escolha == '4':
            loan_menu(connection)
        elif escolha == '5':
            if connection.is_connected():
                connection.close()
            print("Conexão encerrada.")
            break
        else:
            print("Opção inválida, tente novamente.")

if __name__ == "__main__":
    main()