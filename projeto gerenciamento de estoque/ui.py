import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from database import inicializar_banco, adicionar_produto, listar_produtos, remover_produto

class AplicacaoEstoque:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciamento de Estoque Pedro Lima Lopes")
        self.root.attributes("-fullscreen", True)
        self.root.config(bg="#333333")
        self.root.resizable(False, False)

        self.inicializar_banco()
        self.criar_widgets()
        self.atualizar_lista_produtos()

    def inicializar_banco(self):
        inicializar_banco()

    def criar_widgets(self):
        frame_botoes_principal = tk.Frame(self.root, bg="#333333")
        frame_botoes_principal.pack(pady=20)

        # Botão Sair
        self.btn_sair = tk.Button(
            frame_botoes_principal, text="Sair", width=15, height=2,
            bg="#607D8B", fg="white", font=("Arial", 12, "bold"), cursor="hand2",
            command=self.root.quit
        )
        self.btn_sair.pack(side=tk.LEFT, padx=10)
        self.btn_sair.bind("<Enter>", lambda e: self.btn_sair.config(bg="#455A64"))
        self.btn_sair.bind("<Leave>", lambda e: self.btn_sair.config(bg="#607D8B"))

        # Botão Adicionar
        self.btn_adicionar_principal = tk.Button(
            frame_botoes_principal, text="Adicionar Produto", width=15, height=2,
            bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), cursor="hand2",
            command=self.abrir_tela_adicionar
        )
        self.btn_adicionar_principal.pack(side=tk.LEFT, padx=10)
        self.btn_adicionar_principal.bind("<Enter>", lambda e: self.btn_adicionar_principal.config(bg="#45A049"))
        self.btn_adicionar_principal.bind("<Leave>", lambda e: self.btn_adicionar_principal.config(bg="#4CAF50"))

        # Botão Remover
        self.btn_remover_principal = tk.Button(
            frame_botoes_principal, text="Remover Produto", width=15, height=2,
            bg="#97222E", fg="white", font=("Arial", 12, "bold"), cursor="hand2",
            command=self.abrir_tela_remover
        )
        self.btn_remover_principal.pack(side=tk.LEFT, padx=10)
        self.btn_remover_principal.bind("<Enter>", lambda e: self.btn_remover_principal.config(bg="#D32F2F"))
        self.btn_remover_principal.bind("<Leave>", lambda e: self.btn_remover_principal.config(bg="#97222E"))

        self.btn_alterar_principal = tk.Button(
        frame_botoes_principal, text="Alterar Produto",
        width=15, height=2, command=self.abrir_tela_alterar,
        bg="#555555", fg="white", activebackground="#666666", activeforeground="white")
        self.btn_alterar_principal.pack(side=tk.LEFT, padx=10)

        # Lista de produtos
        frame_lista = tk.Frame(self.root, bg="#444444")
        frame_lista.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        self.label_lista = tk.Label(frame_lista, text="Lista de Produtos:", font=("Arial", 16), fg="white", bg="#444444")
        self.label_lista.pack(pady=5, anchor="w")

        # Estilo da Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#555555", foreground="white", fieldbackground="#555555", font=("Arial", 14))
        style.configure("Treeview.Heading", background="#666666", foreground="white", font=("Arial", 14, "bold"))

        self.tree = ttk.Treeview(frame_lista, columns=("ID", "Nome", "Quantidade", "Entradas", "Saídas"), show="headings")

        # Cabeçalhos
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Quantidade", text="Quantidade")
        self.tree.heading("Entradas", text="Entradas")
        self.tree.heading("Saídas", text="Saídas")

        # Colunas com alinhamento à esquerda
        self.tree.column("ID", width=60, anchor="w")
        self.tree.column("Nome", width=200, anchor="w")
        self.tree.column("Quantidade", width=120, anchor="w")
        self.tree.column("Entradas", width=100, anchor="w")
        self.tree.column("Saídas", width=100, anchor="w")

        # Scrollbar para Treeview
        scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Mensagem
        self.frame_mensagem = tk.Frame(self.root, bg="#333333")
        self.frame_mensagem.pack(pady=10)
        self.mensagem_label = tk.Label(self.frame_mensagem, text="", fg="green", bg="#333333")
        self.mensagem_label.pack()

        # Marca d'água no canto superior esquerdo
        label_marca = tk.Label(self.root, text="Pedro Lima Lopes", font=("Arial", 8, "italic"),
                            fg="#888888", bg="#333333")
        label_marca.place(x=10, y=5)


    def atualizar_lista_produtos(self):
        self.tree.delete(*self.tree.get_children())

        produtos = listar_produtos()
        if not produtos:
            self.tree.insert("", "end", values=("-", "Nenhum produto cadastrado", "-", "-", "-"))
        else:
            for produto in produtos:
                id_prod, nome, quantidade, entradas, saidas = produto
                self.tree.insert("", "end", values=(id_prod, nome, quantidade, entradas, saidas))


    def abrir_tela_adicionar(self):
        self.tela_adicionar = tk.Toplevel(self.root)
        self.tela_adicionar.title("Adicionar Produto")
        self.tela_adicionar.geometry("400x300")
        self.tela_adicionar.config(bg="#333333")
        self.tela_adicionar.transient(self.root)
        self.tela_adicionar.grab_set()
        self.tela_adicionar.focus_set()
        self.tela_adicionar.resizable(False, False)

        frame = tk.Frame(self.tela_adicionar, bg="#333333")
        frame.pack(expand=True, padx=20, pady=20)

        label_id = tk.Label(frame, text="ID:", font=("Arial", 12), fg="white", bg="#333333")
        label_id.pack(pady=(10, 5), anchor="w", fill='x')
        self.entry_id_adicionar = tk.Entry(frame)
        self.entry_id_adicionar.pack(pady=5, fill="x")

        label_nome = tk.Label(frame, text="Nome:", font=("Arial", 12), fg="white", bg="#333333")
        label_nome.pack(pady=(10, 5), anchor="w", fill='x')
        self.entry_nome_adicionar = tk.Entry(frame)
        self.entry_nome_adicionar.pack(pady=5, fill="x")

        label_quantidade = tk.Label(frame, text="Quantidade:", font=("Arial", 12), fg="white", bg="#333333")
        label_quantidade.pack(pady=(10, 5), anchor="w", fill='x')
        self.entry_quantidade_adicionar = tk.Entry(frame)
        self.entry_quantidade_adicionar.pack(pady=5, fill="x")

        btn_adicionar = tk.Button(frame, text="Adicionar", command=self.adicionar_novo_produto,
                                bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), width=10, height=2, cursor="hand2")
        btn_adicionar.pack(pady=15)
        btn_adicionar.bind("<Enter>", lambda e: btn_adicionar.config(bg="#45A049"))
        btn_adicionar.bind("<Leave>", lambda e: btn_adicionar.config(bg="#4CAF50"))

        # Confirma com Enter em qualquer campo
        self.tela_adicionar.bind("<Return>", lambda event: self.adicionar_novo_produto())

        # Foco inicial no primeiro campo
        self.entry_id_adicionar.focus()


    def adicionar_novo_produto(self):
        try:
            id_produto = int(self.entry_id_adicionar.get())
            nome = self.entry_nome_adicionar.get()
            quantidade = int(self.entry_quantidade_adicionar.get())
            if adicionar_produto(id_produto, nome, quantidade, entradas=quantidade, saidas=0):
                self.mensagem_label.config(text=f"Produto '{nome}' (ID {id_produto}) adicionado com sucesso.", fg="green")
                self.atualizar_lista_produtos()
                self.tela_adicionar.destroy()
            else:
                self.mensagem_label.config(text="Erro ao adicionar produto (ID duplicado?).", fg="red")
        except ValueError:
            self.mensagem_label.config(text="Erro: ID e Quantidade devem ser números inteiros.", fg="red")

    def abrir_tela_remover(self):
        self.tela_remover = tk.Toplevel(self.root)
        self.tela_remover.title("Remover Produto")
        self.tela_remover.geometry("400x180")
        self.tela_remover.config(bg="#333333")
        self.tela_remover.transient(self.root)
        self.tela_remover.grab_set()
        self.tela_remover.focus_set()
        self.tela_remover.resizable(False, False)

        frame = tk.Frame(self.tela_remover, bg="#333333")
        frame.pack(expand=True, padx=20, pady=20)

        label_id = tk.Label(frame, text="ID do Produto para remover:", font=("Arial", 12), fg="white", bg="#333333")
        label_id.pack(pady=(10, 5), anchor="w", fill='x')
        self.entry_id_remover = tk.Entry(frame)
        self.entry_id_remover.pack(pady=5, fill="x")

        btn_remover = tk.Button(frame, text="Remover", command=self.remover_produto_existente,
                                bg="#F44336", fg="white", font=("Arial", 11, "bold"), width=10, height=2, cursor="hand2")
        btn_remover.pack(pady=15)
        btn_remover.bind("<Enter>", lambda e: btn_remover.config(bg="#D32F2F"))
        btn_remover.bind("<Leave>", lambda e: btn_remover.config(bg="#F44336"))

        # Confirma com Enter
        self.tela_remover.bind("<Return>", lambda event: self.remover_produto_existente())

        # Foco inicial no campo de ID
        self.entry_id_remover.focus()


    def abrir_tela_alterar(self):
        self.tela_alterar = tk.Toplevel(self.root)
        self.tela_alterar.title("Atualizar Estoque")
        self.tela_alterar.geometry("400x400")
        self.tela_alterar.config(bg="#333333")
        self.tela_alterar.transient(self.root)
        self.tela_alterar.grab_set()
        self.tela_alterar.focus_set()
        self.tela_alterar.resizable(False, False)

        frame = tk.Frame(self.tela_alterar, bg="#333333")
        frame.pack(expand=True, padx=20, pady=20)

        label_id = tk.Label(frame, text="ID do Produto:", font=("Arial", 12), fg="white", bg="#333333")
        label_id.pack(pady=(10, 5), anchor="w", fill='x')
        self.entry_id_movimentacao = tk.Entry(frame)
        self.entry_id_movimentacao.pack(pady=5, fill="x")

        label_entrada = tk.Label(frame, text="Adicionar Quantidade:", font=("Arial", 12), fg="white", bg="#333333")
        label_entrada.pack(pady=(10, 5), anchor="w", fill='x')
        self.entry_entrada = tk.Entry(frame)
        self.entry_entrada.pack(pady=5, fill="x")

        label_saida = tk.Label(frame, text="Retirar Quantidade:", font=("Arial", 12), fg="white", bg="#333333")
        label_saida.pack(pady=(10, 5), anchor="w", fill='x')
        self.entry_saida = tk.Entry(frame)
        self.entry_saida.pack(pady=5, fill="x")

        btn_movimentar = tk.Button(frame, text="Atualizar", command=self.movimentar_estoque, width=10, height=2)
        btn_movimentar.pack(pady=20)

        # Agora sim, faça o bind após a criação dos Entry widgets
        self.entry_id_movimentacao.bind("<Return>", lambda event: self.movimentar_estoque())
        self.entry_entrada.bind("<Return>", lambda event: self.movimentar_estoque())
        self.entry_saida.bind("<Return>", lambda event: self.movimentar_estoque())

        self.entry_id_movimentacao.focus()




    def movimentar_estoque(self):
        try:
            id_produto = int(self.entry_id_movimentacao.get())
            entrada = int(self.entry_entrada.get()) if self.entry_entrada.get().strip() else 0
            saida = int(self.entry_saida.get()) if self.entry_saida.get().strip() else 0

            from database import registrar_movimentacao

            if registrar_movimentacao(id_produto, entrada, saida):
                self.mensagem_label.config(text=f"Estoque do produto {id_produto} atualizado com sucesso.", fg="green")
                self.atualizar_lista_produtos()
                self.tela_alterar.destroy()
            else:
                self.mensagem_label.config(text=f"Erro: operação inválida ou produto não encontrado.", fg="red")
        except ValueError:
            self.mensagem_label.config(text="Erro: valores devem ser números inteiros.", fg="red")

    def remover_produto_existente(self):
        try:
            id_produto = int(self.entry_id_remover.get())
            if remover_produto(id_produto):
                self.mensagem_label.config(text=f"Produto com ID {id_produto} removido com sucesso.", fg="green")
                self.atualizar_lista_produtos()
                self.tela_remover.destroy()
            else:
                self.mensagem_label.config(text=f"Produto com ID {id_produto} não encontrado.", fg="red")
        except ValueError:
            self.mensagem_label.config(text="Erro: ID inválido. Digite um número inteiro.", fg="red")

    def alterar_produto_existente(self):
        try:
            id_produto = int(self.entry_id_alterar.get())
            novo_nome = self.entry_nome_alterar.get()
            quantidade_texto = self.entry_quantidade_alterar.get()
            nova_quantidade = int(quantidade_texto) if quantidade_texto.strip() else None

            from database import alterar_produto

            if alterar_produto(id_produto, novo_nome, nova_quantidade):
                self.mensagem_label.config(text=f"Produto {id_produto} alterado com sucesso.", fg="green")
                self.atualizar_lista_produtos()
                self.tela_alterar.destroy()
            else:
                self.mensagem_label.config(text=f"Produto com ID {id_produto} não encontrado.", fg="red")
        except ValueError:
            self.mensagem_label.config(text="Erro: ID deve ser um número inteiro.", fg="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacaoEstoque(root)
    root.mainloop()
