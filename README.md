# 🏥 Sistema de Gestão Hospitalar

## 📘 Descrição do Projeto

Este projeto consiste em um sistema simples de controle de estoque hospitalar desenvolvido em **Python**, utilizando a biblioteca **Tkinter** para interface gráfica e **SQLite** como banco de dados.

O sistema permite:

- Cadastrar novos medicamentos;
- Atualizar informações de estoque;
- Excluir medicamentos;
- Visualizar todos os medicamentos cadastrados;
- Solicitar medicamentos, com controle de quantidade disponível.

---

## ⚙️ Tecnologias Utilizadas

- **Python 3**
- **Tkinter** — para criar a interface gráfica;
- **SQLite3** — banco de dados local embutido;

---

## 🧩 Estrutura do Projeto

```
projeto_hospitalar/
│
├── main.py         # Arquivo principal com a interface Tkinter
├── funcoes.py      # Módulo com todas as funções do sistema
└── estoque.db      # Banco de dados SQLite gerado automaticamente
```

---

## 📄 Arquivo `main.py`

### Função principal (`main()`)

Cria a janela principal do sistema, define o tamanho e adiciona os botões de interação.

```python
def main():
    root = tk.Tk()
    root.title("Sistema de Gestão Hospitalar")
    root.geometry("1000x200")

    # Botões principais da interface
    tk.Button(root, text="Adicionar Medicamento", width=25, command=lambda: funcoes.inserir_dados_banco(conexao)).pack(pady=5)
    tk.Button(root, text="Atualizar Estoque", width=25, command=lambda: funcoes.atualizar_estoque(conexao)).pack(pady=5)
    tk.Button(root, text="Excluir Medicamento", width=25, command=lambda: funcoes.excluir_estoque(conexao)).pack(pady=5)
    tk.Button(root, text="Visualizar Estoque", width=25, command=lambda: funcoes.visualizar_estoque(conexao)).pack(pady=5)
    tk.Button(root, text="Solicitar Medicamento", width=25, command=lambda: funcoes.solicitar_medicamento(conexao)).pack(pady=5)
    tk.Button(root, text="Sair", width=25, command=root.destroy).pack(pady=20)

    root.mainloop()
```

### Execução principal

```python
if __name__ == "__main__":
    conexao = funcoes.conectar_banco('estoque.db')
    funcoes.criar_tabelas(conexao)
    main()
```

---

## 📄 Arquivo `funcoes.py`

### Conectar e Criar Tabela

```python
def conectar_banco(nome_banco):
    conexao = sqlite3.connect(nome_banco)
    return conexao

def criar_tabelas(conexao):
    cursor = conexao.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Estoque(
                id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                quantidade INTEGER NOT NULL)''')
```
Cria a tabela **Estoque** com os campos: `id_produto`, `nome`, `quantidade`.

---

### Inserir Medicamento

```python
def inserir_dados_banco(conexao):
    while True:
        nome_produto = simpledialog.askstring("Adicionar Medicamento", "Digite o nome do medicamento (ou Cancelar para sair):")
        if nome_produto is None:
            break    

        quantidade_produto = simpledialog.askstring("Adicionar Medicamento", f"Digite a quantidade de {nome_produto}:")
        cursor = conexao.cursor()
        cursor.execute('''INSERT INTO Estoque(nome, quantidade) VALUES(?, ?)''', (nome_produto.capitalize(), quantidade_produto))
        conexao.commit()
        messagebox.showinfo("Sucesso", f"{nome_produto.capitalize()} adicionado com sucesso!")
```

---

### Visualizar Estoque

```python
def visualizar_estoque(conexao):
    cursor = conexao.cursor()
    cursor.execute('SELECT id_produto, nome, quantidade FROM Estoque')
    produtos = cursor.fetchall()
    texto = ""
    for produto in produtos:
        texto += f"\nID: {produto[0]} | Nome: {produto[1]} | Quantidade: {produto[2]}\n"
    messagebox.showinfo("Estoque Atual", texto)
```

---

### Atualizar Medicamento

```python
def atualizar_estoque(conexao):
    visualizar_estoque(conexao)
    cursor = conexao.cursor()
    opc = simpledialog.askinteger("Atualizar Estoque", "Deseja alterar o nome (1) ou quantidade (2)?")

    if opc == 1:
        id_med = simpledialog.askinteger("Atualizar Estoque", "Digite o ID do medicamento:")
        novo_nome = simpledialog.askstring("Atualizar Estoque", "Qual o novo nome?")
        cursor.execute('UPDATE Estoque SET nome = ? WHERE id_produto = ?', (novo_nome, id_med))
    else:
        id_med = simpledialog.askinteger("Atualizar Estoque", "Digite o ID do medicamento:")
        nova_qtd = simpledialog.askinteger("Atualizar Estoque", "Nova quantidade:")
        cursor.execute('UPDATE Estoque SET quantidade = ? WHERE id_produto = ?', (nova_qtd, id_med))
    conexao.commit()
    messagebox.showinfo("Sucesso", "Alteração realizada com sucesso!")
```

---

### Solicitar Medicamento

```python
def solicitar_medicamento(conexao):
    visualizar_estoque(conexao)
    cursor = conexao.cursor()
    id_med = simpledialog.askinteger('Solicitar Medicamento', 'Qual medicamento deseja solicitar (ID)?')
    qtd_solicitada = simpledialog.askinteger('Solicitar Medicamento', 'Quantidade desejada:')
    cursor.execute('''UPDATE Estoque SET quantidade = quantidade - ? WHERE id_produto = ? AND quantidade >= ?;''',
                   (qtd_solicitada, id_med, qtd_solicitada))
    if cursor.rowcount == 0:
        messagebox.showinfo('Erro', 'Item em falta no estoque.')
    else:
        conexao.commit()
        messagebox.showinfo('Sucesso', 'Medicamento liberado.')
```

---

### Excluir Medicamento

```python
def excluir_estoque(conexao):
    while True:
        visualizar_estoque(conexao)
        id_med = simpledialog.askinteger('Remover', 'Digite o ID do medicamento que deseja remover:')
        if id_med is None:
            break
        cursor = conexao.cursor()
        cursor.execute('DELETE FROM Estoque WHERE id_produto = ?;', (id_med,))
        conexao.commit()
        messagebox.showinfo('Sucesso', 'Medicamento removido com sucesso!')
```

---

## 🧠 Classe `Estoque`

```python
class Estoque:
    def __init__(self, id, nome, quantidade):
        self.id = id
        self.nome = nome
        self.quantidade = quantidade
```

---

## 🧾 Tabela de Funções

| Função                    | Descrição                     |
| ------------------------- | ----------------------------- |
| `inserir_dados_banco()`   | Adiciona novo medicamento     |
| `visualizar_estoque()`    | Mostra todos os medicamentos  |
| `atualizar_estoque()`     | Atualiza nome ou quantidade   |
| `solicitar_medicamento()` | Retira medicamento do estoque |
| `excluir_estoque()`       | Remove medicamento            |
| `conectar_banco()`        | Conecta ao banco SQLite       |
| `criar_tabelas()`         | Cria a tabela Estoque         |

---

## 🚀 Como Executar o Sistema

1. Certifique-se de ter o **Python 3** instalado.
2. Crie uma pasta com os arquivos `main.py` e `funcoes.py`.
3. Execute o comando no terminal:

```bash
python main.py
```
