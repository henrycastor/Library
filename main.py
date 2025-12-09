import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from crud import (create_book, read_all_books, update_book, delete_book, read_all_authors, 
                  create_author_direct, update_author, delete_author, create_member, read_all_members, 
                  update_member, delete_member, create_loan, read_all_loans, update_loan, delete_loan)
                  #connect, get_author_id)

class LibraryManagementSystem:
    def __init__(self, root: tk.Tk, connection):
        self.root = root
        self.connection = connection
        self.root.title("Sistema de Gerenciamento de Biblioteca")
        self.root.geometry("400x600")

        tk.Button(self.root, text="Criar Livro", command=self.create_book_window).pack(pady=5)
        tk.Button(self.root, text="Ler Todos os Livros", command=self.read_all_books_window).pack(pady=5)
        tk.Button(self.root, text="Atualizar Livro", command=self.update_book_window).pack(pady=5)
        tk.Button(self.root, text="Deletar Livro", command=self.delete_book_window).pack(pady=5)

        tk.Button(self.root, text="Criar Autor", command=self.create_author_window).pack(pady=5)
        tk.Button(self.root, text="Ler Todos os Autores", command=self.read_all_authors_window).pack(pady=5)
        tk.Button(self.root, text="Atualizar Autor", command=self.update_author_window).pack(pady=5)
        tk.Button(self.root, text="Deletar Autor", command=self.delete_author_window).pack(pady=5)

        tk.Button(self.root, text="Criar Membro", command=self.create_member_window).pack(pady=5)
        tk.Button(self.root, text="Ler Todos os Membros", command=self.read_all_members_window).pack(pady=5)
        tk.Button(self.root, text="Atualizar Membro", command=self.update_member_window).pack(pady=5)
        tk.Button(self.root, text="Deletar Membro", command=self.delete_member_window).pack(pady=5)

        tk.Button(self.root, text="Criar Empréstimo", command=self.create_loan_window).pack(pady=5)
        tk.Button(self.root, text="Ler Todos os Empréstimos", command=self.read_all_loans_window).pack(pady=5)
        tk.Button(self.root, text="Atualizar Empréstimo", command=self.update_loan_window).pack(pady=5)
        tk.Button(self.root, text="Deletar Empréstimo", command=self.delete_loan_window).pack(pady=5)

    def connect():
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='biblioteca',
                user='root',
                password='940860117'
            )
            if connection.is_connected():
                print("Conexão bem-sucedida!")
                return connection
        except Error as e:
            print("Erro ao conectar ao MySQL:", e)
            return None
    
    def create_book_window(self):
        window = tk.Toplevel(self.root)
        window.title("Criar Livro")

        tk.Label(window, text="Título").pack()
        titulo = tk.Entry(window)
        titulo.pack()

        tk.Label(window, text="Nome do Autor").pack()
        nome_autor = tk.Entry(window)
        nome_autor.pack()

        tk.Label(window, text="Sobrenome do Autor").pack()
        sobrenome_autor = tk.Entry(window)
        sobrenome_autor.pack()

        tk.Label(window, text="ISBN").pack()
        isbn = tk.Entry(window)
        isbn.pack()

        tk.Label(window, text="Gênero").pack()
        genero = tk.Entry(window)
        genero.pack()

        tk.Label(window, text="Ano de Publicação").pack()
        ano_publicacao = tk.Entry(window)
        ano_publicacao.pack()

        def submit():
            if create_book(self.connection, titulo.get(), nome_autor.get(), sobrenome_autor.get(), isbn.get(), genero.get(), ano_publicacao.get()):
                messagebox.showinfo("Sucesso", "Livro criado com sucesso!")
                window.destroy()
            else:
                messagebox.showerror("Erro", "Erro ao criar o livro")

        tk.Button(window, text="Criar", command=submit).pack()

    def read_all_books_window(self):
        window = tk.Toplevel(self.root)
        window.title("Todos os Livros")

        books = read_all_books(self.connection)
        for idx, book in enumerate(books):
            book_info = f"ID: {book[0]}, Título: {book[1]}, Autor: {book[2]} {book[3]}, ISBN: {book[4]}, Gênero: {book[5]}, Ano: {book[6]}"
            tk.Label(window, text=book_info).grid(row=idx, column=0, sticky="w")
            tk.Button(window, text="Atualizar", command=lambda b=book[0]: self.update_book_window(b)).grid(row=idx, column=1)
            tk.Button(window, text="Deletar", command=lambda b=book[0]: self.delete_book(b)).grid(row=idx, column=2)
            tk.Button(window, text="Emprestar", command=lambda b=book[0]: self.create_loan_window(b)).grid(row=idx, column=3)

    def update_book_window(self, book_id=None):
        window = tk.Toplevel(self.root)
        window.title("Atualizar Livro")

        tk.Label(window, text="ID do Livro").pack()
        livro_id = tk.Entry(window)
        livro_id.pack()
        if book_id:
            livro_id.insert(0, book_id)

        tk.Label(window, text="Novo Título do Livro").pack()
        novo_titulo = tk.Entry(window)
        novo_titulo.pack()

        def submit():
            if update_book(self.connection, livro_id.get(), novo_titulo.get()):
                messagebox.showinfo("Sucesso", "Livro atualizado com sucesso!")
                window.destroy()
            else:
                messagebox.showerror("Erro", "Erro ao atualizar o livro")

        tk.Button(window, text="Atualizar", command=submit).pack()

    def delete_book_window(self):
        window = tk.Toplevel(self.root)
        window.title("Deletar Livro")

        tk.Label(window, text="ID do Livro").pack()
        livro_id = tk.Entry(window)
        livro_id.pack()

        def submit():
            if delete_book(self.connection, livro_id.get()):
                messagebox.showinfo("Sucesso", "Livro deletado com sucesso!")
                window.destroy()
            else:
                messagebox.showerror("Erro", "Erro ao deletar o livro")

        tk.Button(window, text="Deletar", command=submit).pack()

    def create_author_window(self):
        window = tk.Toplevel(self.root)
        window.title("Criar Autor")

        tk.Label(window, text="Nome do Autor").pack()
        nome_autor = tk.Entry(window)
        nome_autor.pack()

        tk.Label(window, text="Sobrenome do Autor").pack()
        sobrenome_autor = tk.Entry(window)
        sobrenome_autor.pack()

        tk.Label(window, text="Nacionalidade").pack()
        nacionalidade = tk.Entry(window)
        nacionalidade.pack()

        def submit():
            if create_author_direct(self.connection, nome_autor.get(), sobrenome_autor.get(), nacionalidade.get()):
                messagebox.showinfo("Sucesso", "Autor criado com sucesso!")
                window.destroy()
            else:
                messagebox.showerror("Erro", "Erro ao criar o autor")

        tk.Button(window, text="Criar", command=submit).pack()

    def read_all_authors_window(self):
        window = tk.Toplevel(self.root)
        window.title("Todos os Autores")

        authors = read_all_authors(self.connection)
        for author in authors:
            tk.Label(window, text=author).pack()

    def update_author_window(self):
        window = tk.Toplevel(self.root)
        window.title("Atualizar Autor")

        tk.Label(window, text="ID do Autor").pack()
        autor_id = tk.Entry(window)
        autor_id.pack()

        tk.Label(window, text="Novo Nome do Autor").pack()
        novo_nome = tk.Entry(window)
        novo_nome.pack()

        def submit():
            if update_author(self.connection, autor_id.get(), novo_nome.get()):
                messagebox.showinfo("Sucesso", "Autor atualizado com sucesso!")
                window.destroy()
            else:
                messagebox.showerror("Erro", "Erro ao atualizar o autor")

        tk.Button(window, text="Atualizar", command=submit).pack()

    def delete_author_window(self):
        window = tk.Toplevel(self.root)
        window.title("Deletar Autor")

        tk.Label(window, text="ID do Autor").pack()
        autor_id = tk.Entry(window)
        autor_id.pack()

        def submit():
            if delete_author(self.connection, autor_id.get()):
                messagebox.showinfo("Sucesso", "Autor deletado com sucesso!")
                window.destroy()
            else:
                messagebox.showerror("Erro", "Erro ao deletar o autor")

        tk.Button(window, text="Deletar", command=submit).pack()

    def create_member_window(self):
        window = tk.Toplevel(self.root)
        window.title("Criar Membro")

        tk.Label(window, text="Nome do Membro").pack()
        nome_membro = tk.Entry(window)
        nome_membro.pack()

        tk.Label(window, text="Sobrenome do Membro").pack()
        sobrenome_membro = tk.Entry(window)
        sobrenome_membro.pack()

        tk.Label(window, text="Endereço do Membro").pack()
        endereco_membro = tk.Entry(window)
        endereco_membro.pack()

        tk.Label(window, text="Email do Membro").pack()
        email_membro = tk.Entry(window)
        email_membro.pack()

        def submit():
            if create_member(self.connection, nome_membro.get(), sobrenome_membro.get(), endereco_membro.get(), email_membro.get()):
                messagebox.showinfo("Sucesso", "Membro criado com sucesso!")
                window.destroy()
            else:
                messagebox.showerror("Erro", "Erro ao criar o membro")

        tk.Button(window, text="Criar", command=submit).pack()

    def read_all_members_window(self):
        window = tk.Toplevel(self.root)
        window.title("Todos os Membros")

        members = read_all_members(self.connection)
        for member in members:
            tk.Label(window, text=member).pack()

    def update_member_window(self):
        window = tk.Toplevel(self.root)
        window.title("Atualizar Membro")

        tk.Label(window, text="ID do Membro").pack()
        membro_id = tk.Entry(window)
        membro_id.pack()

        tk.Label(window, text="Novo Email do Membro").pack()
        novo_email = tk.Entry(window)
        novo_email.pack()

        def submit():
            if update_member(self.connection, membro_id.get(), novo_email.get()):
                messagebox.showinfo("Sucesso", "Membro atualizado com sucesso!")
                window.destroy()
            else:
                messagebox.showerror("Erro", "Erro ao atualizar o membro")

        tk.Button(window, text="Atualizar", command=submit).pack()

    def delete_member_window(self):
        window = tk.Toplevel(self.root)
        window.title("Deletar Membro")

        tk.Label(window, text="ID do Membro").pack()
        membro_id = tk.Entry(window)
        membro_id.pack()

        def submit():
            if delete_member(self.connection, membro_id.get()):
                messagebox.showinfo("Sucesso", "Membro deletado com sucesso!")
                window.destroy()
            else:
                messagebox.showerror("Erro", "Erro ao deletar o membro")

        tk.Button(window, text="Deletar", command=submit).pack()

    def create_loan_window(self, book_id=None):
        window = tk.Toplevel(self.root)
        window.title("Criar Empréstimo")

        tk.Label(window, text="ID do Livro").pack()
        livro_id = tk.Entry(window)
        livro_id.pack()
        if book_id:
            livro_id.insert(0, book_id)

        tk.Label(window, text="ID do Membro").pack()
        membro_id = tk.Entry(window)
        membro_id.pack()

        tk.Label(window, text="Data de Empréstimo (YYYY-MM-DD)").pack()
        data_emprestimo = tk.Entry(window)
        data_emprestimo.pack()

        tk.Label(window, text="Data de Devolução (YYYY-MM-DD)").pack()
        data_devolucao = tk.Entry(window)
        data_devolucao.pack()

        tk.Label(window, text="Status do Empréstimo").pack()
        status_emprestimo = tk.Entry(window)
        status_emprestimo.pack()

        def submit():
            if create_loan(self.connection, livro_id.get(), membro_id.get(), data_emprestimo.get(), data_devolucao.get(), status_emprestimo.get()):
                messagebox.showinfo("Sucesso", "Empréstimo criado com sucesso!")
                window.destroy()
            else:
                messagebox.showerror("Erro", "Erro ao criar o empréstimo")

        tk.Button(window, text="Criar", command=submit).pack()

    def read_all_loans_window(self):
        window = tk.Toplevel(self.root)
        window.title("Todos os Empréstimos")

        loans = read_all_loans(self.connection)
        for loan in loans:
            tk.Label(window, text=loan).pack()

    def update_loan_window(self):
        window = tk.Toplevel(self.root)
        window.title("Atualizar Empréstimo")

        tk.Label(window, text="ID do Empréstimo").pack()
        emprestimo_id = tk.Entry(window)
        emprestimo_id.pack()

        tk.Label(window, text="Novo Status do Empréstimo").pack()
        novo_status = tk.Entry(window)
        novo_status.pack()

        def submit():
            if update_loan(self.connection, emprestimo_id.get(), novo_status.get()):
                messagebox.showinfo("Sucesso", "Empréstimo atualizado com sucesso!")
                window.destroy()
            else:
                messagebox.showerror("Erro", "Erro ao atualizar o empréstimo")

        tk.Button(window, text="Atualizar", command=submit).pack()

    def delete_loan_window(self):
        window = tk.Toplevel(self.root)
        window.title("Deletar Empréstimo")

        tk.Label(window, text="ID do Empréstimo").pack()
        emprestimo_id = tk.Entry(window)
        emprestimo_id.pack()

        def submit():
            if delete_loan(self.connection, emprestimo_id.get()):
                messagebox.showinfo("Sucesso", "Empréstimo deletado com sucesso!")
                window.destroy()
            else:
                messagebox.showerror("Erro", "Erro ao deletar o empréstimo")

        tk.Button(window, text="Deletar", command=submit).pack()