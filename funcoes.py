
import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog


#Criação do banco de dados
def conectar_banco(nome_banco):
    conexao = sqlite3.connect(nome_banco)
    return conexao 

def criar_tabelas(conexao):
    cursor = conexao.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Estoque(
                id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                quantidade INTEGER NOT NULL)''')
    

class Estoque:
    def __init__(self, id , nome, quantidade):
        self.id = id
        self.nome = nome
        self.quantidade = quantidade

    #trocar os input pelo simpledialog e messagebox.

#Concluido
def inserir_dados_banco(conexao):
    while True:
        try:
            cursor = conexao.cursor()
            nome_produto =  simpledialog.askstring("Adicionar Medicamento", "Digite o nome do medicamento (ou Cancelar para sair):")
            if nome_produto is None:  # se o usuário apertar Cancelar
                break    

            quantidade_produto = simpledialog.askstring("Adicionar Medicamento", f"Digite a quantidade de {nome_produto}:")


            comando = '''INSERT INTO Estoque(nome, quantidade)
            VALUES(?,?)'''
            cursor.execute(comando,( nome_produto.capitalize(),
                                 quantidade_produto))
            conexao.commit()
            messagebox.showinfo("Sucesso", f"{nome_produto.capitalize()} adicionado com sucesso!")

        except conexao.DatabaseError as err:
            messagebox.showerror("error","❌ Erro de banco de dados:", err)

   

#Concluido
def visualizar_estoque(conexao):
    cursor = conexao.cursor()
    cursor.execute('''SELECT id_produto, nome, quantidade FROM Estoque''')
    produtos_estoque = cursor.fetchall()
    texto = ""
    for produto in produtos_estoque:
        texto +=(f"\nID: {produto[0]}  |Nome: {produto[1]} | Quantidade: {produto[2]} \n") # printar em lista
    
    messagebox.showinfo("Estoque Atual", texto)

#Concluido
def atualizar_estoque(conexao):
    visualizar_estoque(conexao)
    try:
        cursor = conexao.cursor()
                
        opc_update =  simpledialog.askinteger("Atualizar Estoque", "Deseja alterar o nome (1) ou quantidade (2)?")

        if opc_update == 1:
            procurar_id = simpledialog.askinteger("Atualizar Estoque", "Digite o ID do medicamento:")
            alterar_nome = simpledialog.askstring("Atualizar Estoque", "Qual o novo nome do medicamento?")
            
            cursor.execute('''UPDATE Estoque SET nome = ? WHERE id_produto = ?;''', (alterar_nome, procurar_id))
            conexao.commit()
            messagebox.showinfo('Sucesso','Alteração realizada com sucesso!')
        else:
            try:
                procurar_id = simpledialog.askinteger('Atualizar Estoque', 'Digite o ID do medicamento:')
                alterar_quantidade = simpledialog.askinteger('Atualizar Estoque','Qual a modificação de quantidade que deseja realizar:')
                cursor.execute('''UPDATE Estoque SET quantidade = ? WHERE id_produto = ?;''', (alterar_quantidade, procurar_id))
                conexao.commit()
                messagebox.showinfo('Sucesso','Alteração realizada com sucesso!')

            except ValueError:
                messagebox.showinfo('error','❌ Ops, somente numeros inteiros.')

            except Exception as e:
                 messagebox.showinfo(f"'error","❌ Ocorreu um erro inesperado: {e}")
          

    except ValueError:
        messagebox.showinfo('Error! Digite um numero inteiro')


def solicitar_medicamento(conexao):
    visualizar_estoque(conexao)
    try:
        cursor = conexao.cursor()
                
        opc_solicitar = simpledialog.askinteger('solicitar medicamento', 'Qual medicamento deseja solicitar:')
        quantidade_solicitada = simpledialog.askinteger('solicitar medicamento','Qual a quantidade deseja:')
        cursor.execute('''UPDATE Estoque
        SET quantidade = quantidade - ?
        WHERE id_produto = ? AND quantidade >= ?;
            ''',(quantidade_solicitada, opc_solicitar, quantidade_solicitada) )
      
        if cursor.rowcount == 0:
             messagebox.showinfo('Error','Item estar em falta')

        else:
             messagebox.showinfo('Sucesso','Medicação liberada.')
        
    except ValueError:
         messagebox.showinfo('Error','Error! Digite um numero inteiro')

#Concluido 
def excluir_estoque(conexao):
    while True:
        try:
            cursor = conexao.cursor()
            visualizar_estoque(conexao)
            item_remover = simpledialog.askinteger('Remover','Qual digite o ID do medicamento que deseja remover: ')
            cursor.execute('''DELETE FROM Estoque WHERE  id_produto = ?;''', (item_remover,))
            conexao.commit()
            messagebox.showinfo('Sucesso','Exclusão realizada com sucesso!')
            if item_remover is None:  # se o usuário apertar Cancelar
                break    

        except ValueError:
            messagebox.showinfo('Error','❌ Ops, somente numeros inteiros.')

        except Exception as e:
            messagebox.showinfo(f"Error","❌ Ocorreu um erro inesperado: {e}")
            break










    

    

    
