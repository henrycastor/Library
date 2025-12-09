from mysql.connector import Error
from utils.database import connect

def create_query(connection, table_name, columns, values_list):
    cursor = connection.cursor()
    placeholders = ", ".join(["%s"] * len(values_list[0]))
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    cursor.execute(query)
    connection.commit()

def read_query(connection, table_name):
    try:
        cursor = connection.cursor()
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        table = cursor.fetchall()
        for item in table:
            print(item)
    except Error as e:
        print("Erro ao ler tabela:", e)

def update_query(connection, columns, table_name, item_id):
    try:
        cursor = connection.cursor()

        updates = []
        values = []
        for column in len(columns):
            new_value = input(f"Digite o novo valor para a coluna '{column}': ")
            updates.append(f"{column} = %s")
            values.append(new_value)
        
        # Gera a string de atualização dinâmica
        update_clause = ", ".join(updates)
        query = f"UPDATE {table_name} SET {update_clause} WHERE id = %s"
        
        # Adiciona o ID ao final dos valores
        values.append(item_id)
        
        # Executa a consulta
        cursor.execute(query, values)
        connection.commit()
        print("Item atualizado com sucesso!")
    except Error as e:
        print("Erro ao atualizar item:", e)

# def update_query(connection, table_name, item_id):
#     try:
#         cursor = connection.cursor()
#         item_id = input("Digite o ID do item que deseja atualizar: ")
#         column = input("Digite o nome da coluna que deseja atualizar: ")
#         new_value = input("Digite o novo valor: ")
#         query = f"UPDATE {table_name} SET {column} = '{new_value}' WHERE id = {item_id}"
#         cursor.execute(query)
#         connection.commit()

#         print("Item atualizado com sucesso!")
#     except Error as e:
#         print("Erro ao atualizar item:", e)

def delete_query(connection, table_name, item_id):
    try:
        cursor = connection.cursor()
        item_id = input("Digite o ID do item que deseja deletar: ")
        query = f"DELETE FROM {table_name} WHERE id = {item_id}"
        cursor.execute(query)
        connection.commit()
        print("Item deletado com sucesso!")
    except Error as e:
        print("Erro ao deletar item:", e)