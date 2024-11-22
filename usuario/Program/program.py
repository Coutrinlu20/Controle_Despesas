import tkinter as tk
from tkinter import messagebox
import re 
## import requests 

def limpar_documento():
    """
    Remove a formatação do CPF ou CNPJ inserido e exibe o resultado.
    """
    documento = entrada_documento.get()
    if not documento:
        messagebox.showwarning("Aviso", " Insira um CPF ou CNPJ! ")
        return
    
    documento_limpo = re.sub(r'[.\-\/]', '', documento)
    resultado.set(documento_limpo)
    label_resultado.config(text="O documento foi limpo com sucesso!")
    ## messagebox.showinfo("Resultado:", f"{documento_limpo}")

    janela.after(2500, lambda: label_resultado.config(text="- Resultado Final -"))


# Criação da janela principal
janela = tk.Tk()
janela.title("Remover Formatação de CPF/CNPJ")
janela.geometry("400x200")

# Variável para armazenar o resultado
resultado = tk.StringVar()

# Labels e campos de entrada
label_instrucoes = tk.Label(janela, text="Insira o *CPF* ou *CNPJ*:")
label_instrucoes.pack(pady=10)

entrada_documento = tk.Entry(janela, width=30)
entrada_documento.pack(pady=5)

botao_limpar = tk.Button(janela, text="Limpar", command=limpar_documento)
botao_limpar.pack(pady=10)

label_resultado = tk.Label(janela, text="- Resultado Final -")
label_resultado.pack(pady=10)

campo_resultado = tk.Entry(janela, textvariable=resultado, state="readonly", width=30)
campo_resultado.pack(pady=2)
### Raphael
# Iniciar o loop principal da interface
janela.mainloop()



### tentar criar um programa na qual ela apresenta o numero formatado e ainda se nesse CPF ou CNPJ tem uns processos e apresentar no campo CNJB ###
