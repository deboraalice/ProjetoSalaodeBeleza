import tkinter as tk
from tkinter import ttk, messagebox
import manipulacao_arquivos.manipulador_arquivos_agendamento as maa
import utils as ut
from models.agendamento import Agendamento
        

class JanelaAtualizarAgendamento:
    def __init__(self, janela, agendamento):
        self.agendamento = agendamento
        self.frame = tk.Frame(janela, width=420, height=350)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        label_nome_cliente = tk.Label(self.frame, text="Cliente: ")
        label_nome_cliente.grid(row=0, column=0, sticky='E', padx=5, pady=5)

        self.entrada_nome_cliente = tk.Entry(self.frame)
        self.entrada_nome_cliente.grid(row=0, column=1, sticky='W', padx=5, pady=5)
        self.entrada_nome_cliente.insert(0, agendamento.cliente)
        self.entrada_nome_cliente.focus()

        label_data = tk.Label(self.frame, text="Data: ")
        label_data.grid(row=1, column=0, sticky='E', padx=5, pady=5)

        self.entrada_data = tk.Entry(self.frame)
        self.entrada_data.grid(row=1, column=1, sticky='W', padx=5, pady=5)
        self.entrada_data.insert(0, agendamento.data)

        label_horario = tk.Label(self.frame, text="Horário: ")
        label_horario.grid(row=2, column=0, sticky='E', padx=5, pady=5)
        
        self.entrada_horario = tk.Entry(self.frame)
        self.entrada_horario.grid(row=2, column=1, sticky='W', padx=5, pady=5)
        self.entrada_horario.insert(0, getattr(agendamento, 'horario', getattr(agendamento, 'hora', '')))

        self.status_validos = ["Pendente", "Confirmado", "Cancelado"]

        label_status = tk.Label(self.frame, text="Status: ")
        label_status.grid(row=3, column=0, sticky='E', padx=5, pady=5)

        self.entrada_status = ttk.Combobox(self.frame, values=self.status_validos, state='readonly')
        self.entrada_status.grid(row=3, column=1, sticky='W', padx=5, pady=5)
        self.entrada_status.set(agendamento.status)

        label_servico = tk.Label(self.frame, text="Serviço: ")
        label_servico.grid(row=4, column=0, sticky='E', padx=5, pady=5)
        
        self.entrada_servico = tk.Entry(self.frame)
        self.entrada_servico.grid(row=4, column=1, sticky='W', padx=5, pady=5)
        self.entrada_servico.insert(0, agendamento.servico)

        label_preco = tk.Label(self.frame, text="Preço: ")
        label_preco.grid(row=5, column=0, sticky='E', padx=5, pady=5)

        self.entrada_preco = tk.Entry(self.frame)
        self.entrada_preco.grid(row=5, column=1, sticky='W', padx=5, pady=5)
        # formatar preço no formato brasileiro com R$
        if agendamento.preco is not None:
            try:
                preco_num = float(agendamento.preco)
                preco_formatado = f"R$ {preco_num:.2f}".replace('.', ',')
            except (ValueError, TypeError):
                preco_formatado = str(agendamento.preco)
        else:
            preco_formatado = "R$ 0,00"
        self.entrada_preco.insert(0, preco_formatado)

        label_duracao = tk.Label(self.frame, text="Duração: ")
        label_duracao.grid(row=6, column=0, sticky='E', padx=5, pady=5)
        
        self.entrada_duracao = tk.Entry(self.frame)
        self.entrada_duracao.grid(row=6, column=1, sticky='W', padx=5, pady=5)
        duracao_str = str(agendamento.duracao) if agendamento.duracao is not None else "0"
        self.entrada_duracao.insert(0, duracao_str)

        label_profissional = tk.Label(self.frame, text="Profissional: ")
        label_profissional.grid(row=7, column=0, sticky='E', padx=5, pady=5)
        
        self.entrada_profissional = tk.Entry(self.frame)
        self.entrada_profissional.grid(row=7, column=1, sticky='W', padx=5, pady=5)
        self.entrada_profissional.insert(0, agendamento.profissional)
        
        botao = tk.Button(self.frame, text="Atualizar", command=self.atualizar_agendamento)
        botao.grid(row=8, column=0, padx=5, pady=5, columnspan=2)
        
        
    def limpar_preco(self, preco_texto):
        """Remove caracteres não numéricos do preço e converte para float"""
        import re
        # Remove tudo exceto dígitos, vírgulas e pontos
        preco_limpo = re.sub(r'[^\d,.]', '', preco_texto)
        # Substitui vírgula por ponto
        preco_limpo = preco_limpo.replace(',', '.')
        # Se ficou vazio, retorna 0
        if not preco_limpo:
            return 0.0
        return float(preco_limpo)
        

    def limpar_campos(self):
        self.entrada_nome_cliente.delete(0, 'end')
        self.entrada_data.delete(0, 'end')
        self.entrada_horario.delete(0, 'end')
        self.entrada_status.set('')
        self.entrada_servico.delete(0, 'end')
        self.entrada_preco.delete(0, 'end')
        self.entrada_duracao.delete(0, 'end')
        self.entrada_profissional.delete(0, 'end')


    def atualizar_agendamento(self):
        try:
            # Recuperar dados dos campos
            cliente = self.entrada_nome_cliente.get().strip()
            data = self.entrada_data.get().strip()
            horario = self.entrada_horario.get().strip()
            status = self.entrada_status.get()
            servico = self.entrada_servico.get().strip()
            preco = self.entrada_preco.get().strip()
            duracao = self.entrada_duracao.get().strip()
            profissional = self.entrada_profissional.get().strip()

            # Validações
            if not all([cliente, data, horario, status, servico, preco, duracao, profissional]):
                messagebox.showwarning("Atenção", "Preencha todos os campos obrigatórios.")
                return

            # Validar e limpar preço
            try:
                preco_float = self.limpar_preco(preco)
                
                # Verificar se é um valor positivo
                if preco_float < 0:
                    messagebox.showerror("Erro", "O preço deve ser um valor positivo.")
                    return
                    
                print(f"Preço original: '{preco}' -> Preço processado: {preco_float}")
                    
            except ValueError:
                messagebox.showerror("Erro", f"O preço '{preco}' não contém um número válido.\nExemplo: R$ 25,50 ou 25.50")
                return
                
            # Validar duração se for numérica
            duracao_processada = duracao
            if duracao.replace('.', '').replace(',', '').isdigit():
                try:
                    duracao_limpa = duracao.replace(',', '.')
                    duracao_float = float(duracao_limpa)
                    duracao_processada = duracao_float
                except ValueError:
                    pass 

            novo_agendamento = Agendamento(
                cliente=cliente,
                data=data,
                horario=horario,
                servico=servico,
                preco=preco_float,
                duracao=duracao_processada,
                profissional=profissional,
                status=status,
                id=self.agendamento.id 
            )
            
            print(f"Atualizando agendamento ID {self.agendamento.id}")
            
            resultado = maa.atualizar_agendamento(novo_agendamento)

            ut.exibir_mensagem(resultado, "Agendamento atualizado com sucesso!", "Erro ao atualizar agendamento.")
              
            if resultado:
                self.frame.destroy()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar agendamento: {str(e)}")
            print(f"Erro detalhado: {e}")