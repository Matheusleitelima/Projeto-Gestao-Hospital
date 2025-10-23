import funcoes
import tkinter as tk
from tkinter import messagebox


def main():
    #criar a janela principal
    root = tk.Tk()
    root.title("Sistema de Gestão Hospitalar")
    root.geometry("1000x200")  # tamanho da janela


    #botoes
    tk.Button(root, text="Adicionar Medicamento", width=25, command=lambda: funcoes.inserir_dados_banco(conexao)).pack(pady=5) 
    #Crie um botão com o texto ‘Adicionar Medicamento’, largura 25, que quando clicado chama a função inserir_dados_gui passando conexao, e coloque ele na janela com um espaçamento vertical de 5 pixels.
    tk.Button(root, text="Atualizar Estoque", width=25, command=lambda: funcoes.atualizar_estoque(conexao)).pack(pady=5)
    tk.Button(root, text="Excluir Medicamento", width=25, command=lambda: funcoes.excluir_estoque(conexao)).pack(pady=5)
    tk.Button(root, text="Visualizar Estoque", width=25, command=lambda: funcoes.visualizar_estoque(conexao)).pack(pady=5)
    tk.Button(root, text="Solicitar Medicamento", width=25, command=lambda: funcoes.solicitar_medicamento(conexao)).pack(pady=5)
    tk.Button(root, text="Sair", width=25, command=root.destroy).pack(pady=20)
    #olambda cria uma função temporaria

    #rodar um loop
    root.mainloop()

if __name__ == "__main__":
    conexao = funcoes.conectar_banco('estoque.db')
    funcoes.criar_tabelas(conexao)
    main()







