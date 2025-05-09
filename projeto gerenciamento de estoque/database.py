import sqlite3

DATABASE_NAME = 'estoque.db'

def inicializar_banco():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY,
        nome TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        entradas INTEGER DEFAULT 0,
        saidas INTEGER DEFAULT 0
    )
    ''')
    try:
        cursor.execute('ALTER TABLE produtos ADD COLUMN entradas INTEGER DEFAULT 0')
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute('ALTER TABLE produtos ADD COLUMN saidas INTEGER DEFAULT 0')
    except sqlite3.OperationalError:
        pass

    conn.commit()
    conn.close()

def adicionar_produto(id_produto, nome, quantidade, entradas=0, saidas=0):
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO produtos (id, nome, quantidade, entradas, saidas)
                VALUES (?, ?, ?, ?, ?)
            ''', (id_produto, nome, quantidade, entradas, saidas))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        print(f"Erro: Produto com ID {id_produto} já existe.")
        return False
    except sqlite3.Error as e:
        print(f"Erro ao adicionar produto: {e}")
        return False

def listar_produtos():
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, nome, quantidade, entradas, saidas FROM produtos')
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao listar produtos: {e}")
        return []

def remover_produto(id_produto):
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM produtos WHERE id = ?', (id_produto,))
            conn.commit()
            return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Erro ao remover produto: {e}")
        return False

def alterar_produto(id_produto, novo_nome, nova_quantidade):
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT nome, quantidade FROM produtos WHERE id = ?', (id_produto,))
            resultado = cursor.fetchone()

            if resultado:
                nome_atual, quantidade_atual = resultado


                if not novo_nome.strip():
                    novo_nome = nome_atual
                if nova_quantidade is None:
                    nova_quantidade = quantidade_atual

                cursor.execute('''
                    UPDATE produtos SET nome = ?, quantidade = ? WHERE id = ?
                ''', (novo_nome, nova_quantidade, id_produto))
                conn.commit()
                return True
            else:
                return False
    except sqlite3.Error as e:
        print(f"Erro ao alterar produto: {e}")
        return False

def registrar_movimentacao(id_produto, entrada=0, saida=0):
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT quantidade, entradas, saidas FROM produtos WHERE id = ?', (id_produto,))
            resultado = cursor.fetchone()

            if not resultado:
                return False

            quantidade_atual, entradas_atuais, saidas_atuais = resultado

            nova_quantidade = quantidade_atual + entrada - saida
            if nova_quantidade < 0:
                return False

            novo_total_entradas = entradas_atuais + entrada
            novo_total_saidas = saidas_atuais + saida

            cursor.execute('''
                UPDATE produtos
                SET quantidade = ?, entradas = ?, saidas = ?
                WHERE id = ?
            ''', (nova_quantidade, novo_total_entradas, novo_total_saidas, id_produto))
            conn.commit()
            return True
    except sqlite3.Error as e:
        print(f"Erro ao registrar movimentação: {e}")
        return False



if __name__ == "__main__":
    inicializar_banco()