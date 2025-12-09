from crud.loan import create_loan, read_all_loans, update_loan, delete_loan
from utils.queries import read_query, delete_query
from utils.create_table import create_loan_table_if_not_exists

def loan_menu(connection):
    create_loan_table_if_not_exists(connection)

    print("\nMenu de Empréstimos:")
    print("1. Criar um novo empréstimo")
    print("2. Ler todos os empréstimos")
    print("3. Atualizar um empréstimo")
    print("4. Deletar um empréstimo")
    escolha = input("Digite o número da opção desejada: ")

    if escolha == '1':
        create_loan(connection)
    elif escolha == '2':
        read_query(connection, "Empréstimo")
    elif escolha == '3':
        update_loan(connection)
    elif escolha == '4':
        delete_query(connection, "Empréstimo")
    else:
        print("Opção inválida, tente novamente.")