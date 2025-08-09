import tkinter as tk
import manipulacao_arquivos.manipulador_arquivos_cliente as mac
import utils as ut
from models.cliente import Cliente


import tkinter as tk
import manipulacao_arquivos.manipulador_arquivos_cliente as mac
import utils as ut
from models.cliente import Cliente


class JanelaCadastroCliente:
    def __init__(self, janela):
        self.frame = tk.Frame(janela, width=420, height=350)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        label_nome = tk.Label(self.frame, text="Nome: ")
        label_nome.grid(row=0, column=0, sticky='E', padx=5, pady=5)

        self.entrada_nome = tk.Entry(self.frame)
        self.entrada_nome.grid(row=0, column=1, sticky='W', padx=5, pady=5)
        self.entrada_nome.focus()

        label_cpf = tk.Label(self.frame, text="CPF: ")
        label_cpf.grid(row=1, column=0, sticky='E', padx=5, pady=5)
        
        self.entrada_cpf = tk.Entry(self.frame)
        self.entrada_cpf.grid(row=1, column=1, sticky='W', padx=5, pady=5)
        
        label_telefone = tk.Label(self.frame, text="Telefone: ")
        label_telefone.grid(row=2, column=0, sticky='E', padx=5, pady=5)
        
        self.entrada_telefone = tk.Entry(self.frame)
        self.entrada_telefone.grid(row=2, column=1, sticky='W', padx=5, pady=5)

        label_email = tk.Label(self.frame, text="E-mail: ")
        label_email.grid(row=3, column=0, sticky='E', padx=5, pady=5)
        
        self.entrada_email = tk.Entry(self.frame)
        self.entrada_email.grid(row=3, column=1, sticky='W', padx=5, pady=5)

        botao = tk.Button(self.frame, text="Salvar", command=self.cadastrar_cliente)
        botao.grid(row=4, column=0, padx=5, pady=5, columnspan=2)

    def limpar_campos(self):
        self.entrada_nome.delete(0, 'end')
        self.entrada_email.delete(0, 'end')
        self.entrada_cpf.delete(0, 'end')
        self.entrada_telefone.delete(0, 'end')
        self.entrada_nome.focus()

    def validar_campos(self):
        nome = self.entrada_nome.get().strip()
        cpf = self.entrada_cpf.get().strip()
        telefone = self.entrada_telefone.get().strip()
        email = self.entrada_email.get().strip()
        
        if not nome:
            ut.exibir_mensagem(False, "", "O campo Nome é obrigatório.")
            return False
        
        if not cpf:
            ut.exibir_mensagem(False, "", "O campo CPF é obrigatório.")
            return False
            
        if not telefone:
            ut.exibir_mensagem(False, "", "O campo Telefone é obrigatório.")
            return False
            
        if not email:
            ut.exibir_mensagem(False, "", "O campo E-mail é obrigatório.")
            return False
            
        return True

    def cadastrar_cliente(self):
        try:
            # Valida os campos
            if not self.validar_campos():
                return
            
            # Recupera dados digitados na tela
            nome = self.entrada_nome.get().strip()
            cpf = self.entrada_cpf.get().strip()
            telefone = self.entrada_telefone.get().strip()
            email = self.entrada_email.get().strip()
            
            # Cria objeto da classe Cliente
            novo_cliente = Cliente(nome, cpf, telefone, email)

            # Envia o objeto para ser salvo no arquivo
            resultado = mac.adicionar_cliente(novo_cliente)
            
            # Exibe mensagem de sucesso ou falha
            if resultado:
                ut.exibir_mensagem(True, "Cliente adicionado com sucesso!", "")
                self.limpar_campos()
            else:
                ut.exibir_mensagem(False, "", "Erro ao adicionar cliente.")
                
        except Exception as e:
            print(f"Erro ao cadastrar cliente: {e}")
            ut.exibir_mensagem(False, "", f"Erro inesperado: {str(e)}")