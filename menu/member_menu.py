from crud.member import create_member, read_all_members, update_member, delete_member
from utils.queries import read_query, delete_query
from utils.create_table import create_member_table_if_not_exists

def member_menu(connection):
    create_member_table_if_not_exists(connection)

    print("\nMenu de Membros:")
    print("1. Criar um novo membro")
    print("2. Ler todos os membros")
    print("3. Atualizar um membro")
    print("4. Deletar um membro")
    escolha = input("Digite o número da opção desejada: ")

    if escolha == '1':
        create_member(connection)
    elif escolha == '2':
        read_query(connection, "Membro")
    elif escolha == '3':
        update_member(connection)
    elif escolha == '4':
        delete_query(connection, "Membro")
    else:
        print("Opção inválida, tente novamente.")