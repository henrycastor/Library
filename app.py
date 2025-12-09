import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from utils.database import connect
import mysql.connector
from mysql.connector import Error

class LibraryApp:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.root.title("Sistema de Biblioteca")
        self.root.geometry("800x600")
        
        # Apply a simple theme adjustment if available
        try:
            style = ttk.Style()
            style.theme_use('clam')
        except tk.TclError:
            pass
        
        self.create_widgets()
        self.read_books() # Initial load

    def create_widgets(self):
        # Build the main interface container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header_label = ttk.Label(main_frame, text="Gerenciamento de Biblioteca", font=("Segoe UI", 18, "bold"))
        header_label.pack(pady=(0, 20))

        # Input Area (Form)
        form_frame = ttk.LabelFrame(main_frame, text="Novo Livro / Detalhes", padding="15")
        form_frame.pack(fill=tk.X, pady=5)

        # Grid layout for inputs
        grid_frame = ttk.Frame(form_frame)
        grid_frame.pack(fill=tk.X)

        self.vars = {
            'titulo': tk.StringVar(),
            'autor_nome': tk.StringVar(),
            'autor_sobrenome': tk.StringVar(),
            'isbn': tk.StringVar(),
            'genero': tk.StringVar(),
            'ano': tk.StringVar()
        }

        # Row 0
        ttk.Label(grid_frame, text="Título:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(grid_frame, textvariable=self.vars['titulo'], width=40).grid(row=0, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(grid_frame, text="ISBN:").grid(row=0, column=2, sticky="e", padx=5, pady=5)
        ttk.Entry(grid_frame, textvariable=self.vars['isbn'], width=20).grid(row=0, column=3, sticky="w", padx=5, pady=5)

        # Row 1
        ttk.Label(grid_frame, text="Autor (Nome):").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(grid_frame, textvariable=self.vars['autor_nome'], width=40).grid(row=1, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(grid_frame, text="Autor (Sobrenome):").grid(row=1, column=2, sticky="e", padx=5, pady=5)
        ttk.Entry(grid_frame, textvariable=self.vars['autor_sobrenome'], width=20).grid(row=1, column=3, sticky="w", padx=5, pady=5)

        # Row 2
        ttk.Label(grid_frame, text="Gênero:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(grid_frame, textvariable=self.vars['genero'], width=40).grid(row=2, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(grid_frame, text="Ano:").grid(row=2, column=2, sticky="e", padx=5, pady=5)
        ttk.Entry(grid_frame, textvariable=self.vars['ano'], width=20).grid(row=2, column=3, sticky="w", padx=5, pady=5)

        # Action Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Adicionar Livro", command=self.create_book).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpar Campos", command=self.clear_fields).pack(side=tk.LEFT, padx=5)

        # List Area
        list_frame = ttk.LabelFrame(main_frame, text="Lista de Livros", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Treeview
        columns = ("id", "titulo", "autor", "isbn", "genero", "ano")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        self.tree.heading("id", text="#")
        self.tree.heading("titulo", text="Título")
        self.tree.heading("autor", text="Autor")
        self.tree.heading("isbn", text="ISBN")
        self.tree.heading("genero", text="Gênero")
        self.tree.heading("ano", text="Ano")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("titulo", width=200)
        self.tree.column("autor", width=150)
        self.tree.column("isbn", width=100)
        self.tree.column("genero", width=100)
        self.tree.column("ano", width=60, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Context Menu Buttons (Bottom)
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(pady=5)

        ttk.Button(bottom_frame, text="Atualizar Selecionado", command=self.update_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text="Deletar Selecionado", command=self.delete_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text="Recarregar Lista", command=self.read_books).pack(side=tk.LEFT, padx=5)

    def clear_fields(self):
        for var in self.vars.values():
            var.set("")

    def get_or_create_author_id(self, nome, sobrenome):
        if not nome or not sobrenome:
            return None
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT id FROM Autor WHERE nome = %s AND sobrenome = %s", (nome, sobrenome))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                # Prompt for nationality if creating new
                nacionalidade = simpledialog.askstring("Novo Autor", 
                    f"O autor '{nome} {sobrenome}' é novo.\nPor favor, digite a nacionalidade:",
                    parent=self.root)
                if nacionalidade is None: 
                    nacionalidade = "" # Default to empty string instead of crashing
                
                cursor.execute("INSERT INTO Autor (nome, sobrenome, nacionalidade) VALUES (%s, %s, %s)", 
                               (nome, sobrenome, nacionalidade))
                self.connection.commit()
                return cursor.lastrowid
        except Error as e:
            messagebox.showerror("Erro de Banco de Dados", f"Erro ao processar autor: {e}")
            return None

    def create_book(self):
        vals = {k: v.get().strip() for k, v in self.vars.items()}
        
        if not vals['titulo'] or not vals['autor_nome'] or not vals['autor_sobrenome']:
            messagebox.showwarning("Aviso", "Título e Nome/Sobrenome do Autor são obrigatórios!")
            return

        autor_id = self.get_or_create_author_id(vals['autor_nome'], vals['autor_sobrenome'])
        if not autor_id:
            return # Cancelled or error

        try:
            cursor = self.connection.cursor()
            # Check for ISBN duplicate if ISBN is provided
            if vals['isbn']:
                cursor.execute("SELECT id FROM Livro WHERE isbn = %s", (vals['isbn'],))
                if cursor.fetchone():
                    messagebox.showerror("Erro", f"Já existe um livro com ISBN {vals['isbn']}")
                    return

            query = """INSERT INTO Livro (titulo, autor_id, isbn, genero, ano_publicacao) 
                       VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query, (vals['titulo'], autor_id, vals['isbn'], vals['genero'], vals['ano']))
            self.connection.commit()
            
            messagebox.showinfo("Sucesso", "Livro adicionado com sucesso!")
            self.clear_fields()
            self.read_books()
        except Error as e:
            messagebox.showerror("Erro Crítico", f"Erro ao salvar livro: {e}")

    def read_books(self):
        # Clear current list
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT L.id, L.titulo, CONCAT(A.nome, ' ', A.sobrenome), L.isbn, L.genero, L.ano_publicacao 
                FROM Livro L
                LEFT JOIN Autor A ON L.autor_id = A.id
                ORDER BY L.id DESC
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                # Handle None values for display
                display_row = [str(x) if x is not None else "" for x in row]
                self.tree.insert("", tk.END, values=display_row)
        except Error as e:
            messagebox.showerror("Erro", f"Erro ao carregar livros: {e}")

    def delete_selected(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um livro para deletar.")
            return
            
        book_id = self.tree.item(selected_item[0])['values'][0]
        
        if not messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir o livro ID {book_id}?"):
            return
            
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM Livro WHERE id = %s", (book_id,))
            self.connection.commit()
            self.tree.delete(selected_item[0])
            messagebox.showinfo("Sucesso", "Livro removido.")
        except Error as e:
            messagebox.showerror("Erro", f"Erro ao deletar: {e}")

    def update_selected(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um livro para atualizar.")
            return
            
        book_id = self.tree.item(selected_item[0])['values'][0]
        current_title = self.tree.item(selected_item[0])['values'][1] # Title is at index 1
        
        new_title = simpledialog.askstring("Atualizar Título", f"Novo título para (ID {book_id}):", initialvalue=current_title)
        
        if new_title and new_title.strip():
            try:
                cursor = self.connection.cursor()
                cursor.execute("UPDATE Livro SET titulo = %s WHERE id = %s", (new_title.strip(), book_id))
                self.connection.commit()
                messagebox.showinfo("Sucesso", "Título atualizado.")
                self.read_books()
            except Error as e:
                messagebox.showerror("Erro", f"Erro ao atualizar: {e}")

def main():
    db_connection = connect()
    if db_connection:
        root = tk.Tk()
        # Set icon if available (optional)
        # root.iconbitmap('icon.ico') 
        app = LibraryApp(root, db_connection)
        root.mainloop()
        if db_connection.is_connected():
            db_connection.close()
    else:
        # If connection fails, show a simple error window
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Erro Fatal", "Não foi possível conectar ao banco de dados.\nVerifique as configurações em utils/database.py")
        root.destroy()

if __name__ == "__main__":
    main()