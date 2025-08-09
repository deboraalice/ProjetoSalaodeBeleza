import tkinter as tk
import manipulacao_arquivos.manipulador_arquivos_agendamento as maa
import utils as ut
from manipulacao_arquivos import manipulador_arquivos_cliente as mac
from models.agendamento import Agendamento
from tkinter import ttk


class JanelaCadastroAgendamento:
    def __init__(self, janela):
        self.frame = tk.Frame(janela, width=420, height=350)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        label_cliente = tk.Label(self.frame, text="Cliente: ")
        label_cliente.grid(row=0, column=0, sticky='E', padx=5, pady=5)

        self.combobox_cliente = ttk.Combobox(self.frame, values=self.carregar_clientes(), state='readonly')
        self.combobox_cliente.grid(row=0, column=1, sticky='W', padx=5, pady=5)
        self.combobox_cliente.set('')

        label_data = tk.Label(self.frame, text="Data: ")
        label_data.grid(row=1, column=0, sticky='E', padx=5, pady=5)

        self.entrada_data = tk.Entry(self.frame)
        self.entrada_data.insert(0, "DD/MM/AAAA")
        self.entrada_data.grid(row=1, column=1, sticky='W', padx=5, pady=5)

        self.horarios_disponiveis = [
            "08:00", "09:00", "10:00", "11:00", "13:00", "14:00", "15:00", "16:00", "17:00"
       ]

        label_horario = tk.Label(self.frame, text="Horário: ")
        label_horario.grid(row=2, column=0, sticky='E', padx=5, pady=5)
        
        self.entrada_horario = ttk.Combobox(self.frame, values=self.horarios_disponiveis, state='readonly')
        self.entrada_horario.grid(row=2, column=1, sticky='W', padx=5, pady=5)
        self.entrada_horario.set("")

        label_status = tk.Label(self.frame, text="Status: ")
        label_status.grid(row=3, column=0, sticky='E', padx=5, pady=5)

        self.entrada_status = tk.Entry(self.frame)
        self.entrada_status.grid(row=3, column=1, sticky='W', padx=5, pady=5)
        self.entrada_status.config(state='normal')
        self.entrada_status.insert(0, "Pendente")
        self.entrada_status.config(state='readonly')

        label_servico = tk.Label(self.frame, text="Serviço: ")
        label_servico.grid(row=4, column=0, sticky='E', padx=5, pady=5)

        self.servicos_precos = {
            "Corte": 30.0,
            "Escova": 40.0,
            "Coloração": 70.0,
            "Manicure": 25.0
        }
        
        self.entrada_servico = ttk.Combobox(self.frame, values=list(self.servicos_precos.keys()), state='readonly')
        self.entrada_servico.grid(row=4, column=1, sticky="W", padx=5, pady=5)
        self.entrada_servico.bind("<<ComboboxSelected>>", self.atualizar_preco)

        self.precos_servicos = [
            "R$ 30,00 (Corte)", "R$ 40,00 (Escova)", "R$ 70,00 (Coloração)", "R$ 25,00 (Manicure)"
       ]

        label_preco = tk.Label(self.frame, text="Preço: ")
        label_preco.grid(row=5, column=0, sticky='E', padx=5, pady=5)
        
        self.entrada_preco = tk.Entry(self.frame, state='readonly')
        self.entrada_preco.grid(row=5, column=1, sticky='W', padx=5, pady=5)

        label_duracao = tk.Label(self.frame, text="Duração: ")
        label_duracao.grid(row=6, column=0, sticky='E', padx=5, pady=5)
        
        duracoes = ["30 minutos", "1 hora", "1 hora e 30 minutos"]
        self.entrada_duracao = ttk.Combobox(self.frame, values=duracoes)
        self.entrada_duracao.grid(row=6, column=1, sticky='W', padx=5, pady=5)

        self.servicos_profissionais = ["Débora", "Kimberly", "Nicolle", "Olívia"]

        label_profissional = tk.Label(self.frame, text="Profissional: ")
        label_profissional.grid(row=7, column=0, sticky='E', padx=5, pady=5)
        
        self.entrada_profissional = ttk.Combobox(self.frame, values=self.servicos_profissionais, state='readonly')
        self.entrada_profissional.grid(row=7, column=1, sticky='W', padx=5, pady=5)
        self.entrada_profissional.set("")

        botao = tk.Button(self.frame, text="Salvar", command=self.cadastrar_agendamento)
        botao.grid(row=8, column=0, padx=5, pady=5, columnspan=2)

    def limpar_campos(self):
        self.combobox_cliente.set('')
        self.entrada_data.delete(0, 'end')
        self.entrada_data.insert(0, "DD/MM/AAAA")
        self.entrada_horario.set('')
        self.entrada_status.config(state='normal')
        self.entrada_status.delete(0, 'end')
        self.entrada_status.insert(0, "Pendente")
        self.entrada_status.config(state='readonly')
        self.entrada_servico.set('')
        self.entrada_preco.config(state='normal')
        self.entrada_preco.delete(0, 'end')
        self.entrada_preco.config(state='readonly')
        self.entrada_duracao.set('')
        self.entrada_profissional.set('')
        self.entrada_data.focus()

    def carregar_clientes(self):
        try:
            dados = mac.carregar_clientes()
            
            # Verifica se dados é None ou vazio
            if dados is None:
                print("Aviso: Nenhum cliente encontrado. Retornando lista vazia.")
                self.clientes = []
                return []
            
            if not isinstance(dados, list):
                print(f"Aviso: Dados esperados como lista, mas recebido: {type(dados)}")
                self.clientes = []
                return []
                
            self.clientes = dados  # Os dados já são objetos Cliente vindos do manipulador

            # Extrai apenas os nomes para o combobox
            nomes_clientes = []
            for cliente in self.clientes:
                if hasattr(cliente, 'nome_cliente'):
                    nomes_clientes.append(cliente.nome_cliente)
                else:
                    print(f"Cliente sem atributo nome_cliente: {cliente}")

            return nomes_clientes
            
        except Exception as e:
            print(f"Erro ao carregar clientes: {e}")
            ut.exibir_mensagem(False, "", f"Erro ao carregar clientes: {e}")
            self.clientes = []
            return []

    def atualizar_preco(self, event=None):
        servico = self.entrada_servico.get()
        preco = self.servicos_precos.get(servico, 0.0)
        self.entrada_preco.config(state='normal')
        self.entrada_preco.delete(0, tk.END)
        self.entrada_preco.insert(0, f"R$ {preco:.2f}")
        self.entrada_preco.config(state='readonly')

    def cadastrar_agendamento(self):
        cliente_selecionado = self.combobox_cliente.get()
        if not cliente_selecionado:
            ut.exibir_mensagem(False, "", "Selecione um cliente.")
            return
            
        cliente_obj = next((c for c in self.clientes if c.nome_cliente == cliente_selecionado), None)
        if not cliente_obj:
            ut.exibir_mensagem(False, "", "Cliente selecionado não encontrado.")
            return

        data = self.entrada_data.get().strip()
        horario = self.entrada_horario.get().strip()
        status = self.entrada_status.get().strip()
        servico = self.entrada_servico.get().strip()
        preco = self.entrada_preco.get().strip()
        duracao = self.entrada_duracao.get().strip()
        profissional = self.entrada_profissional.get().strip()

        try:
            from datetime import datetime
            if data == "DD/MM/AAAA":
                ut.exibir_mensagem(False, "", "Informe a data corretamente.")
                return
            datetime.strptime(data, "%d/%m/%Y")
        except ValueError:
            ut.exibir_mensagem(False, "", "Data inválida. Use o formato DD/MM/AAAA.")
            return

        if not data or not horario or not servico or not preco or not duracao or not profissional:
            ut.exibir_mensagem(False, "", "Preencha todos os campos obrigatórios.")
            return

        novo_agendamento = Agendamento(cliente_obj.nome_cliente, data, horario, servico, preco, duracao, profissional, status)
        resultado = maa.adicionar_agendamento(novo_agendamento)
        ut.exibir_mensagem(resultado, "Agendamento adicionado com sucesso!", "Erro ao adicionar agendamento.")
        self.limpar_campos()