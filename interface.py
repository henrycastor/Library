import tkinter as tk
from tkinter import messagebox, simpledialog
from crud import (connect, create_book, read_all_books, update_book, delete_book, read_all_authors, 
                  create_author_direct, update_author, delete_author, create_member, read_all_members, 
                  update_member, delete_member, create_loan, read_all_loans, update_loan, delete_loan, 
                  get_author_id)

class LibraryManagementSystem:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.root.title("Sistema de Gerenciamento de Biblioteca")
        
        # Configuração da interface principal
        self.main_frame = tk.Frame(root)
        self.main_frame.pack()
        
        # Adiciona botões para cada operação CRUD
        self.create_widgets()

    def create_widgets(self):
        tk.Button(self.main_frame, text="Criar Livro", command=self.create_book_window).grid(row=0, column=0)
        tk.Button(self.main_frame, text="Ler Livros", command=self.read_books_window).grid(row=0, column=1)
        tk.Button(self.main_frame, text="Atualizar Livro", command=self.update_book_window).grid(row=1, column=0)
        tk.Button(self.main_frame, text="Deletar Livro", command=self.delete_book_window).grid(row=1, column=1)
        tk.Button(self.main_frame, text="Lista de Membros", command=self.read_all_members_window).grid(row=2, column=0)
        tk.Button(self.main_frame, text="Todos os Empréstimos", command=self.read_all_loans_window).grid(row=2, column=1)
        # Outros botões para autores, membros e empréstimos...

    def create_book_window(self):
        window = tk.Toplevel(self.root)
        window.title("Criar Livro")
        
        tk.Label(window, text="Título").grid(row=0, column=0)
        titulo = tk.Entry(window)
        titulo.grid(row=0, column=1)
        
        tk.Label(window, text="Nome do Autor").grid(row=1, column=0)
        nome_autor = tk.Entry(window)
        nome_autor.grid(row=1, column=1)
        
        tk.Label(window, text="Sobrenome do Autor").grid(row=2, column=0)
        sobrenome_autor = tk.Entry(window)
        sobrenome_autor.grid(row=2, column=1)
        
        tk.Label(window, text="ISBN").grid(row=3, column=0)
        isbn = tk.Entry(window)
        isbn.grid(row=3, column=1)
        
        tk.Label(window, text="Gênero").grid(row=4, column=0)
        genero = tk.Entry(window)
        genero.grid(row=4, column=1)
        
        tk.Label(window, text="Ano de Publicação").grid(row=5, column=0)
        ano_publicacao = tk.Entry(window)
        ano_publicacao.grid(row=5, column=1)
        
        def submit():
            autor_id = get_author_id(self.connection, nome_autor.get(), sobrenome_autor.get())
            if not autor_id:
                nacionalidade = simpledialog.askstring("Entrada Necessária", "Nacionalidade do Autor:")
                autor_id = create_author_direct(self.connection, nome_autor.get(), sobrenome_autor.get(), nacionalidade)
                
            if create_book(self.connection, titulo.get(), nome_autor.get(), sobrenome_autor.get(), isbn.get(), genero.get(), ano_publicacao.get()):
                messagebox.showinfo("Sucesso", "Livro criado com sucesso!")
            else:
                messagebox.showerror("Erro", "Erro ao criar livro.")
            window.destroy()
        
        tk.Button(window, text="Criar", command=submit).grid(row=6, column=0, columnspan=2)
    
    def read_books_window(self):
        window = tk.Toplevel(self.root)
        window.title("Lista de Livros")
        
        books = read_all_books(self.connection)
        for idx, (livro_id, titulo, nome, sobrenome, isbn, genero, ano_publicacao) in enumerate(books):
            tk.Label(window, text=f"{titulo} - {nome} {sobrenome}").grid(row=idx, column=0)
            tk.Button(window, text="Apagar", command=lambda id=livro_id: self.delete_book(id)).grid(row=idx, column=1)
            tk.Button(window, text="Atualizar", command=lambda id=livro_id: self.update_book_window(id)).grid(row=idx, column=2)
            tk.Button(window, text="Emprestar", command=lambda id=livro_id: self.create_loan_window(id)).grid(row=idx, column=3)

    def update_book_window(self, livro_id=None):
        if livro_id is None:
            livro_id = simpledialog.askinteger("Entrada Necessária", "ID do Livro:")
        if livro_id is None:
            return
        
        window = tk.Toplevel(self.root)
        window.title("Atualizar Livro")
        
        tk.Label(window, text="Novo Título").grid(row=0, column=0)
        novo_titulo = tk.Entry(window)
        novo_titulo.grid(row=0, column=1)
        
        def submit():
            if update_book(self.connection, livro_id, novo_titulo.get()):
                messagebox.showinfo("Sucesso", "Livro atualizado com sucesso!")
            else:
                messagebox.showerror("Erro", "Erro ao atualizar livro.")
            window.destroy()
        
        tk.Button(window, text="Atualizar", command=submit).grid(row=1, column=0, columnspan=2)
    
    def delete_book(self, livro_id):
        if delete_book(self.connection, livro_id):
            messagebox.showinfo("Sucesso", "Livro apagado com sucesso!")
        else:
            messagebox.showerror("Erro", "Erro ao apagar livro.")
    
    def delete_book_window(self):
        livro_id = simpledialog.askinteger("Entrada Necessária", "ID do Livro:")
        if livro_id:
            self.delete_book(livro_id)

    def create_loan_window(self, livro_id=None):
        window = tk.Toplevel(self.root)
        window.title("Emprestar Livro")
        
        if livro_id is None:
            tk.Label(window, text="ID do Livro").grid(row=0, column=0)
            livro_id = tk.Entry(window)
            livro_id.grid(row=0, column=1)
        else:
            livro_id_entry = tk.Entry(window)
            livro_id_entry.insert(0, livro_id)
            livro_id_entry.grid(row=0, column=1)
            livro_id_entry.config(state='disabled')
        
        tk.Label(window, text="ID do Membro").grid(row=1, column=0)
        membro_id = tk.Entry(window)
        membro_id.grid(row=1, column=1)
        
        tk.Label(window, text="Data de Empréstimo (AAAA-MM-DD)").grid(row=2, column=0)
        data_emprestimo = tk.Entry(window)
        data_emprestimo.grid(row=2, column=1)
        
        tk.Label(window, text="Data de Devolução (AAAA-MM-DD)").grid(row=3, column=0)
        data_devolucao = tk.Entry(window)
        data_devolucao.grid(row=3, column=1)
        
        tk.Label(window, text="Status").grid(row=4, column=0)
        status = tk.Entry(window)
        status.grid(row=4, column=1)
        
        def submit():
            livro_id_value = livro_id if isinstance(livro_id, int) else int(livro_id.get())
            if create_loan(self.connection, livro_id_value, int(membro_id.get()), data_emprestimo.get(), data_devolucao.get(), status.get()):
                messagebox.showinfo("Sucesso", "Livro emprestado com sucesso!")
            else:
                messagebox.showerror("Erro", "Erro ao emprestar livro.")
            window.destroy()
        
        tk.Button(window, text="Emprestar", command=submit).grid(row=5, column=0, columnspan=2)

    def read_all_members_window(self):
        window = tk.Toplevel(self.root)
        window.title("Lista de Membros")

        members = read_all_members(self.connection)
        if not members:
            tk.Label(window, text="Nenhum membro encontrado.").grid(row=0, column=0)
        else:
            for idx, member in enumerate(members):
                tk.Label(window, text=f"{member}").grid(row=idx, column=0)
    
    def read_all_loans_window(self):
        window = tk.Toplevel(self.root)
        window.title("Todos os Empréstimos")

        loans = read_all_loans(self.connection)
        if not loans:
            tk.Label(window, text="Nenhum empréstimo encontrado.").pack()
        else:
            for loan in loans:
                tk.Label(window, text=loan).pack()

def main():
    connection = connect()
    if connection:
        root = tk.Tk()
        app = LibraryManagementSystem(root, connection)
        root.mainloop()
    else:
        print("Erro ao conectar ao banco de dados.")

if __name__ == "__main__":
    main()