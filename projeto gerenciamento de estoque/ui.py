import tkinter as tk
from tkinter import ttk, Toplevel, messagebox
from database import (
    inicializar_banco,
    adicionar_produto,
    listar_produtos,
    remover_produto,
    alterar_produto
)

class AplicacaoEstoque:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciamento de Estoque Pedro Lima Lopes")
        self.root.attributes("-fullscreen", True)
        self.root.config(bg="#2e2e2e")
        self.root.resizable(False, False)

        self.entry_style = {
            "font": ("Arial", 12),
            "bg": "#3e3e3e",
            "fg": "white",
            "insertbackground": "white",
            "relief": "flat",
            "borderwidth": 1
        }
        
        self.label_style_dialog = {
            "font": ("Arial", 12),
            "fg": "white",
            "bg": "#2e2e2e"
        }

        self.selected_product_id_for_edit = None

        self.inicializar_banco()
        self.criar_widgets()
        self.atualizar_lista_produtos()
        self._update_action_button_states()

    def inicializar_banco(self):
        inicializar_banco()

    def _create_styled_button(self, parent, text, command, bg_color, hover_color, width=20, side=tk.LEFT, padx=10, pady_btn=5, state=tk.NORMAL):
        btn = tk.Button(parent, text=text, bg=bg_color, fg="white", font=("Arial", 12, "bold"),
                        width=width, padx=5, pady=10, command=command, relief="flat",
                        activebackground=hover_color, borderwidth=0, state=state)
        btn.pack(side=side, padx=padx, pady=pady_btn)
        
        def on_enter(e):
            if btn['state'] == tk.NORMAL:
                btn.config(bg=hover_color)
        def on_leave(e):
            if btn['state'] == tk.NORMAL:
                btn.config(bg=bg_color)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    def update_feedback_message(self, message, color="green"):
        self.mensagem_label.config(text=message, fg=color)
        self.mensagem_label.after(4000, lambda: self.mensagem_label.config(text=""))

    def _update_action_button_states_event(self, event=None):
        self._update_action_button_states()

    def _update_action_button_states(self):
        selected_item = self.tree.selection()
        if selected_item:
            if hasattr(self, 'btn_editar_produto') and self.btn_editar_produto:
                self.btn_editar_produto.config(state=tk.NORMAL)
            if hasattr(self, 'btn_remover_principal') and self.btn_remover_principal:
                self.btn_remover_principal.config(state=tk.NORMAL)
        else:
            if hasattr(self, 'btn_editar_produto') and self.btn_editar_produto:
                self.btn_editar_produto.config(state=tk.DISABLED)
            if hasattr(self, 'btn_remover_principal') and self.btn_remover_principal:
                self.btn_remover_principal.config(state=tk.DISABLED)

    def criar_widgets(self):
        spacer = tk.Frame(self.root, height=30, bg="#2e2e2e")
        spacer.pack()

        frame_botoes_principal = tk.Frame(self.root, bg="#2e2e2e")
        frame_botoes_principal.pack(pady=10)

        self.btn_adicionar_principal = self._create_styled_button(
            frame_botoes_principal, "Adicionar Produto", self.abrir_tela_adicionar,
            "#4caf50", "#66bb6a", pady_btn=(0,10)
        )
        self.btn_editar_produto = self._create_styled_button(
            frame_botoes_principal, "Editar Produto", self.abrir_tela_editar_produto,
            "#ff9800", "#ffb74d", pady_btn=(0,10), state=tk.DISABLED
        )
        self.btn_remover_principal = self._create_styled_button(
            frame_botoes_principal, "Remover Produto", self.abrir_tela_remover,
            "#f44336", "#e57373", pady_btn=(0,10), state=tk.DISABLED
        )
        self.btn_sair = self._create_styled_button(
            frame_botoes_principal, "Sair", self.root.quit,
            "#9e9e9e", "#bdbdbd", pady_btn=(0,10)
        )

        frame_lista = tk.Frame(self.root, bg="#2e2e2e")
        frame_lista.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        self.label_lista = tk.Label(frame_lista, text="Lista de Produtos:",
                                    font=("Arial", 14, "bold"),
                                    fg="white", bg="#2e2e2e")
        self.label_lista.pack(pady=5, anchor="w")

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#1e1e1e", foreground="white",
                        fieldbackground="#1e1e1e", rowheight=28, font=("Arial", 11))
        style.map("Treeview", background=[('selected', '#555555')], foreground=[('selected', 'white')])
        style.configure("Treeview.Heading", background="#3e3e3e", foreground="white",
                        font=("Arial", 13, "bold"), padding=(5, 5), relief="flat")
        style.map("Treeview.Heading", background=[('active', '#4a4a4a')])

        self.tree = ttk.Treeview(frame_lista, columns=("ID", "Nome", "Quantidade", "Entradas", "Saídas"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Quantidade", text="Quantidade")
        self.tree.heading("Entradas", text="Entradas")
        self.tree.heading("Saídas", text="Saídas")

        self.tree.column("ID", width=60, anchor="w")
        self.tree.column("Nome", width=200, anchor="w")
        self.tree.column("Quantidade", width=120, anchor="w")
        self.tree.column("Entradas", width=100, anchor="w")
        self.tree.column("Saídas", width=100, anchor="w")
        
        self.tree.bind("<<TreeviewSelect>>", self._update_action_button_states_event)

        scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.mensagem_label = tk.Label(self.root, text="", bg="#2e2e2e", font=("Arial", 12, "bold"))
        self.mensagem_label.pack(pady=(5,10))

        label_marca = tk.Label(
            self.root,
            text="Programa de Estoque por Pedro Lima Lopes",
            font=("Arial", 9, "italic"),
            fg="#B8860B",
            bg="#2e2e2e",
            relief=tk.RIDGE,
            borderwidth=2
        )
        label_marca.place(x=10, y=5)

    def _center_toplevel(self, toplevel_window, width, height):
        toplevel_window.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        toplevel_window.geometry(f'{width}x{height}+{x}+{y}')

    def atualizar_lista_produtos(self):
        self.tree.delete(*self.tree.get_children())
        produtos = listar_produtos()
        if not produtos:
            self.tree.insert("", "end", values=("-", "Nenhum produto cadastrado", "-", "-", "-"))
        else:
            for produto in produtos:
                id_prod, nome, quantidade, entradas, saidas = produto
                self.tree.insert("", "end", values=(id_prod, nome, quantidade, entradas, saidas))
        self._update_action_button_states()

    def abrir_tela_adicionar(self):
        self.tela_adicionar = tk.Toplevel(self.root)
        self.tela_adicionar.title("Adicionar Produto")
        self.tela_adicionar.config(bg="#2e2e2e")
        self.tela_adicionar.transient(self.root)
        self.tela_adicionar.grab_set()
        self.tela_adicionar.resizable(False, False)
        
        dialog_width, dialog_height = 400, 320
        self._center_toplevel(self.tela_adicionar, dialog_width, dialog_height)

        frame = tk.Frame(self.tela_adicionar, bg="#2e2e2e")
        frame.pack(expand=True, padx=20, pady=20)

        tk.Label(frame, text="ID:", **self.label_style_dialog).pack(pady=(10,0), anchor="w", fill='x')
        self.entry_id_adicionar = tk.Entry(frame, **self.entry_style)
        self.entry_id_adicionar.pack(pady=(0,10), fill="x")

        tk.Label(frame, text="Nome:", **self.label_style_dialog).pack(pady=(5,0), anchor="w", fill='x')
        self.entry_nome_adicionar = tk.Entry(frame, **self.entry_style)
        self.entry_nome_adicionar.pack(pady=(0,10), fill="x")

        tk.Label(frame, text="Quantidade Inicial:", **self.label_style_dialog).pack(pady=(5,0), anchor="w", fill='x')
        self.entry_quantidade_adicionar = tk.Entry(frame, **self.entry_style)
        self.entry_quantidade_adicionar.pack(pady=(0,15), fill="x")

        self._create_styled_button(
             frame, "Adicionar", self.adicionar_novo_produto,
             "#4caf50", "#66bb6a", width=15, side=tk.TOP, pady_btn=10
        )
        
        self.tela_adicionar.bind("<Return>", lambda event: self.adicionar_novo_produto())
        self.entry_id_adicionar.focus()

    def adicionar_novo_produto(self):
        try:
            id_produto_str = self.entry_id_adicionar.get()
            nome = self.entry_nome_adicionar.get()
            quantidade_str = self.entry_quantidade_adicionar.get()

            if not id_produto_str or not nome or not quantidade_str:
                self.update_feedback_message("Todos os campos são obrigatórios.", "orange")
                if hasattr(self, 'tela_adicionar') and self.tela_adicionar.winfo_exists():
                    messagebox.showerror("Erro de Entrada", "Todos os campos são obrigatórios.", parent=self.tela_adicionar)
                return

            id_produto = int(id_produto_str)
            quantidade = int(quantidade_str)

            if quantidade < 0:
                self.update_feedback_message("Quantidade não pode ser negativa.", "orange")
                if hasattr(self, 'tela_adicionar') and self.tela_adicionar.winfo_exists():
                    messagebox.showerror("Erro de Entrada", "Quantidade não pode ser negativa.", parent=self.tela_adicionar)
                return

            if adicionar_produto(id_produto, nome, quantidade, entradas=quantidade, saidas=0):
                self.update_feedback_message(f"Produto '{nome}' (ID {id_produto}) adicionado.", "green")
                self.atualizar_lista_produtos()
                if hasattr(self, 'tela_adicionar') and self.tela_adicionar.winfo_exists():
                    self.tela_adicionar.destroy()
            else:
                self.update_feedback_message("Erro ao adicionar produto (ID duplicado?).", "red")
                if hasattr(self, 'tela_adicionar') and self.tela_adicionar.winfo_exists():
                    messagebox.showerror("Erro no Banco", "Erro ao adicionar produto (ID duplicado?).", parent=self.tela_adicionar)
        except ValueError:
            self.update_feedback_message("ID e Quantidade devem ser números inteiros.", "red")
            if hasattr(self, 'tela_adicionar') and self.tela_adicionar.winfo_exists():
                messagebox.showerror("Erro de Entrada", "ID e Quantidade devem ser números inteiros.", parent=self.tela_adicionar)
        except Exception as e:
            self.update_feedback_message(f"Erro inesperado: {e}", "red")
            if hasattr(self, 'tela_adicionar') and self.tela_adicionar.winfo_exists():
                messagebox.showerror("Erro", f"Ocorreu um erro: {e}", parent=self.tela_adicionar)

    def abrir_tela_remover(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        self.tela_remover = tk.Toplevel(self.root)
        self.tela_remover.title("Remover Produto")
        self.tela_remover.config(bg="#2e2e2e")
        self.tela_remover.transient(self.root)
        self.tela_remover.grab_set()
        self.tela_remover.resizable(False, False)

        dialog_width, dialog_height = 400, 180
        self._center_toplevel(self.tela_remover, dialog_width, dialog_height)

        frame = tk.Frame(self.tela_remover, bg="#2e2e2e")
        frame.pack(expand=True, padx=20, pady=20)
        
        item_values = self.tree.item(selected_item[0], 'values')
        id_para_remover = item_values[0]
        nome_para_remover = item_values[1]

        tk.Label(frame, text=f"Remover Produto: {nome_para_remover} (ID: {id_para_remover})", **self.label_style_dialog).pack(pady=(10,15), anchor="center", fill='x')
        
        self._create_styled_button(
             frame, "Confirmar Remoção", lambda: self.remover_produto_existente(id_para_remover),
             "#f44336", "#e57373", width=18, side=tk.TOP, pady_btn=10
        )
        self.tela_remover.bind("<Return>", lambda event: self.remover_produto_existente(id_para_remover))

    def remover_produto_existente(self, id_produto_a_remover):
        try:
            id_produto = int(id_produto_a_remover)
            
            if remover_produto(id_produto):
                self.update_feedback_message(f"Produto com ID {id_produto} removido.", "green")
                self.atualizar_lista_produtos()
                if hasattr(self, 'tela_remover') and self.tela_remover.winfo_exists():
                    self.tela_remover.destroy()
            else:
                self.update_feedback_message(f"Produto com ID {id_produto} não encontrado.", "red")
                if hasattr(self, 'tela_remover') and self.tela_remover.winfo_exists():
                    messagebox.showerror("Erro no Banco", f"Produto com ID {id_produto} não encontrado.", parent=self.tela_remover)
        except ValueError:
            self.update_feedback_message("ID inválido.", "red")
            if hasattr(self, 'tela_remover') and self.tela_remover.winfo_exists():
                messagebox.showerror("Erro de Dados", "ID do produto inválido.", parent=self.tela_remover)
        except Exception as e:
            self.update_feedback_message(f"Erro inesperado: {e}", "red")
            if hasattr(self, 'tela_remover') and self.tela_remover.winfo_exists():
                messagebox.showerror("Erro", f"Ocorreu um erro: {e}", parent=self.tela_remover)

    def abrir_tela_editar_produto(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        
        item_values = self.tree.item(selected_item[0], 'values')
        self.selected_product_id_for_edit = int(item_values[0])
        current_name = item_values[1]
        current_quantity = item_values[2]

        self.tela_editar = tk.Toplevel(self.root)
        self.tela_editar.title("Editar Produto")
        self.tela_editar.config(bg="#2e2e2e")
        self.tela_editar.transient(self.root)
        self.tela_editar.grab_set()
        self.tela_editar.resizable(False, False)

        dialog_width, dialog_height = 400, 300
        self._center_toplevel(self.tela_editar, dialog_width, dialog_height)

        frame = tk.Frame(self.tela_editar, bg="#2e2e2e")
        frame.pack(expand=True, padx=20, pady=20)

        tk.Label(frame, text=f"Editando Produto ID: {self.selected_product_id_for_edit}", **self.label_style_dialog).pack(pady=(10,0), anchor="w", fill='x')
        
        tk.Label(frame, text="Nome:", **self.label_style_dialog).pack(pady=(10,0), anchor="w", fill='x')
        self.entry_nome_editar = tk.Entry(frame, **self.entry_style)
        self.entry_nome_editar.pack(pady=(0,10), fill="x")
        self.entry_nome_editar.insert(0, current_name)

        tk.Label(frame, text="Quantidade Total:", **self.label_style_dialog).pack(pady=(5,0), anchor="w", fill='x')
        self.entry_quantidade_editar = tk.Entry(frame, **self.entry_style)
        self.entry_quantidade_editar.pack(pady=(0,15), fill="x")
        self.entry_quantidade_editar.insert(0, current_quantity)

        self._create_styled_button(
            frame, "Salvar Alterações", self.salvar_produto_editado,
            "#ff9800", "#ffb74d", width=18, side=tk.TOP, pady_btn=10
        )

        self.tela_editar.bind("<Return>", lambda event: self.salvar_produto_editado())
        self.entry_nome_editar.focus()

    def salvar_produto_editado(self):
        try:
            id_produto = self.selected_product_id_for_edit
            novo_nome = self.entry_nome_editar.get().strip()
            nova_quantidade_str = self.entry_quantidade_editar.get().strip()

            if not novo_nome or not nova_quantidade_str:
                self.update_feedback_message("Nome e Quantidade são obrigatórios.", "orange")
                if hasattr(self, 'tela_editar') and self.tela_editar.winfo_exists():
                    messagebox.showerror("Erro de Entrada", "Nome e Quantidade são obrigatórios.", parent=self.tela_editar)
                return
            
            nova_quantidade = int(nova_quantidade_str)

            if nova_quantidade < 0:
                self.update_feedback_message("Quantidade não pode ser negativa.", "orange")
                if hasattr(self, 'tela_editar') and self.tela_editar.winfo_exists():
                    messagebox.showerror("Erro de Entrada", "Quantidade não pode ser negativa.", parent=self.tela_editar)
                return

            if alterar_produto(id_produto, novo_nome, nova_quantidade):
                self.update_feedback_message(f"Produto ID {id_produto} alterado com sucesso.", "green")
                self.atualizar_lista_produtos()
                if hasattr(self, 'tela_editar') and self.tela_editar.winfo_exists():
                    self.tela_editar.destroy()
            else:
                self.update_feedback_message(f"Falha ao alterar produto ID {id_produto}.", "red")
                if hasattr(self, 'tela_editar') and self.tela_editar.winfo_exists():
                    messagebox.showerror("Erro no Banco", f"Falha ao alterar produto ID {id_produto}.", parent=self.tela_editar)
        except ValueError:
            self.update_feedback_message("Quantidade deve ser um número inteiro.", "red")
            if hasattr(self, 'tela_editar') and self.tela_editar.winfo_exists():
                messagebox.showerror("Erro de Entrada", "Quantidade deve ser um número inteiro.", parent=self.tela_editar)
        except Exception as e:
            self.update_feedback_message(f"Erro inesperado: {e}", "red")
            if hasattr(self, 'tela_editar') and self.tela_editar.winfo_exists():
                messagebox.showerror("Erro", f"Ocorreu um erro: {e}", parent=self.tela_editar)
        finally:
            self.selected_product_id_for_edit = None

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacaoEstoque(root)
    root.mainloop()