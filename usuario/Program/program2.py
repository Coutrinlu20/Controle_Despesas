import tkinter as tk
from tkinter import messagebox
import re



#### irei checar ainda 

def limpar_documento():
    """
    Remove a formatação do CPF ou CNPJ inserido e realiza uma consulta de processos.
    """
    documento = entrada_documento.get()
    if not documento:
        messagebox.showwarning("Aviso", "Por favor, insira um CPF ou CNPJ!")
        return
                #Raphael Mendes
    documento_limpo = re.sub(r'[.\-\/]', '', documento)

    # Mostra apenas o número limpo no campo
    campo_formatado.config(state="normal")
    campo_formatado.delete("1.0", tk.END)
    campo_formatado.insert("1.0", documento_limpo, "negrito")
    campo_formatado.config(state="disabled")

    label_resultado.config(text="Consultando processos...")

    # Realiza a consulta de processos
    consulta_processos(documento_limpo)


def consulta_processos(documento):
    """#Raphael Mendes
    Simula uma consulta a uma API para verificar processos por CPF ou CNPJ.
    """
    try:
        # Simula a resposta da API
        dados = {
            "documento": documento,
            "tem_processos": True,
            "detalhes": [
                {"id_processo": "67890", "descricao": "Estelionato"},
                {"id_processo": "13579", "descricao": "Tráfico de drogas"},
            ],
        }

        if dados["tem_processos"]:
            # Verifica apenas os processos de interesse
            processos_importantes = [
                proc
                for proc in dados["detalhes"]
                if "tráfico de drogas" in proc["descricao"].lower()
                or "estelionato" in proc["descricao"].lower()
            ]

            campo_processos.config(state="normal")
            campo_processos.delete("1.0", tk.END)
                #Raphael Mendes
            if processos_importantes:
                for proc in processos_importantes:
                    # Destaca em vermelho e negrito os processos importantes
                    campo_processos.insert(
                        tk.END,
                        f"ID: {proc['id_processo']} - {proc['descricao']}\n",
                        "vermelho_negrito",
                    )

                # Adiciona a mensagem ao final
                campo_processos.insert(
                    tk.END,
                    "\n O CPF ou CNPJ possui processos de estelionato e/ou tráfico de drogas.\n"
                    "Estes dados apareceram no Data Rudder e o Compliance Diego Atalon deve analisar.",
                    "mensagem_final",
                )
                label_resultado.config(text="O documento possui processos relevantes.")
            else:
                campo_processos.insert("1.0", "Sem processos relevantes.")
                label_resultado.config(text="Nenhum processo relevante encontrado.")
        else:
            campo_processos.insert("1.0", "Sem processos registrados.")
            label_resultado.config(text="Nenhum processo encontrado.")

        campo_processos.config(state="disabled")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao consultar processos: {e}")

#Raphael Mendes
# Criação da janela principal
janela = tk.Tk()
janela.title("Consulta de CPF/CNPJ")
janela.geometry("600x400")

# Labels e campos de entrada
label_instrucoes = tk.Label(janela, text="Insira o CPF ou CNPJ:")
label_instrucoes.pack(pady=10)

entrada_documento = tk.Entry(janela, width=30)
entrada_documento.pack(pady=5)

botao_limpar = tk.Button(janela, text="Consultar", command=limpar_documento)
botao_limpar.pack(pady=10)

# Label para mensagem de consulta
label_resultado = tk.Label(janela, text="- Resultado Final -", font=("Arial", 10, "italic"))
label_resultado.pack(pady=10)

# Campo para exibir o número limpo
label_formatado = tk.Label(janela, text="Número limpo:")
label_formatado.pack(pady=5)

campo_formatado = tk.Text(janela, height=1, width=30, state="disabled")
campo_formatado.tag_configure("negrito", font=("Arial", 10, "bold"))
campo_formatado.pack(pady=5)

# Campo para exibir os processos
label_processos = tk.Label(janela, text="**CNPJ e CPF** - Processos relevantes: ")
label_processos.pack(pady=5)

campo_processos = tk.Text(janela, height=10, width=70)
campo_processos.tag_configure("vermelho_negrito", foreground="red", font=("Arial", 10, "bold"))
campo_processos.tag_configure("mensagem_final", font=("Arial", 10, "italic"))
campo_processos.pack(pady=5)

# Iniciar o loop principal da interface
janela.mainloop()


