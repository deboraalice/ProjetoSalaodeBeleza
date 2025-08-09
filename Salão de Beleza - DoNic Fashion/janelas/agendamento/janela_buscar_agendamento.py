import tkinter as tk
import manipulacao_arquivos.manipulador_arquivos_agendamento as maa
from tkinter import messagebox
from janelas.agendamento.janela_atualizar_agendamento import JanelaAtualizarAgendamento
import utils as ut


class JanelaBuscaAgendamento:
    def __init__(self, janela):
        self.janela = janela
        self.agendamento_buscado = None
        self.frame = tk.Frame(janela, width=420, height=350)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        label_id = tk.Label(self.frame, text="ID: ")
        label_id.grid(row=0, column=0, sticky='E', padx=5, pady=5)

        self.entrada_id = tk.Entry(self.frame)
        self.entrada_id.grid(row=0, column=1, sticky='W', padx=5, pady=5)
        self.entrada_id.focus()

        self.botao = tk.Button(self.frame, text="Buscar", command=self.buscar_agendamento)
        self.botao.grid(row=1, column=0, padx=5, pady=5, columnspan=2)

        self.label_id_resultado = tk.Label(self.frame)
        self.label_id_resultado.grid(row=2, column=0, sticky='W', padx=5, pady=5, columnspan=2)

        self.label_data_resultado = tk.Label(self.frame)
        self.label_data_resultado.grid(row=3, column=0, sticky='W', padx=5, pady=5, columnspan=2)

        self.label_horario_resultado = tk.Label(self.frame)
        self.label_horario_resultado.grid(row=4, column=0, sticky='W', padx=5, pady=5, columnspan=2)

        self.label_status_resultado = tk.Label(self.frame)
        self.label_status_resultado.grid(row=5, column=0, sticky='W', padx=5, pady=5, columnspan=2)

        self.label_servico_resultado = tk.Label(self.frame)
        self.label_servico_resultado.grid(row=6, column=0, sticky='W', padx=5, pady=5, columnspan=2)

        self.label_preco_resultado = tk.Label(self.frame)
        self.label_preco_resultado.grid(row=7, column=0, sticky='W', padx=5, pady=5, columnspan=2)

        self.label_duracao_resultado = tk.Label(self.frame)
        self.label_duracao_resultado.grid(row=8, column=0, sticky='W', padx=5, pady=5, columnspan=2)

        self.label_profissional_resultado = tk.Label(self.frame)
        self.label_profissional_resultado.grid(row=9, column=0, sticky='W', padx=5, pady=5, columnspan=2)

        self.label_cliente_resultado = tk.Label(self.frame)
        self.label_cliente_resultado.grid(row=10, column=0, padx=5, pady=5, sticky='W', columnspan=2)

        self.botao_atualizar = tk.Button(self.frame, text="Atualizar", command=self.atualizar_agendamento, state='disabled')
        self.botao_atualizar.grid(row=11, column=0, padx=5, pady=5, sticky='E')

        self.botao_excluir = tk.Button(self.frame, text="Excluir", command=self.excluir_agendamento, state='disabled')
        self.botao_excluir.grid(row=11, column=1, padx=5, pady=5, sticky='W')   

        self.reset_textos_labels()


    def limpar_campos(self):
        self.entrada_id.delete(0 ,'end')

    
    def reset_textos_labels(self):
        self.label_id_resultado.config(text="ID: ")
        self.label_data_resultado.config(text="Data: ")
        self.label_horario_resultado.config(text="Horário: ")
        self.label_status_resultado.config(text="Status: ")
        self.label_servico_resultado.config(text="Serviço: ")
        self.label_preco_resultado.config(text="Preço: ")
        self.label_duracao_resultado.config(text="Duração: ")
        self.label_profissional_resultado.config(text="Profissional: ")
        self.label_cliente_resultado.config(text="Cliente: ")
    
    
    def exibir_resultado(self, resultado):
        self.reset_textos_labels()
    
        self.label_id_resultado.config(text=f"ID: {resultado.id}")
        self.label_data_resultado.config(text=f"Data: {resultado.data}")
        self.label_horario_resultado.config(text=f"Horário: {resultado.horario}")
        self.label_status_resultado.config(text=f"Status: {resultado.status}")
        self.label_servico_resultado.config(text=f"Serviço: {resultado.servico}")
        self.label_preco_resultado.config(text=f"Preço: {resultado.preco}")
        self.label_duracao_resultado.config(text=f"Duração: {resultado.duracao}")
        self.label_profissional_resultado.config(text=f"Profissional: {resultado.profissional}")
        self.label_cliente_resultado.config(text=f"Cliente: {resultado.cliente}")
    
    
    def buscar_agendamento(self):
        id = self.entrada_id.get().strip()
        if not id:
            messagebox.showwarning("Campo vazio", "Por favor, insira um ID.")
            return
        if not id.isdigit():
            messagebox.showerror("ID inválido", "O ID deve conter apenas números.")
            return
    
        id_int = int(id)
        resultado = maa.buscar_agendamento_por_id(id_int)

        if resultado:
            self.agendamento_buscado = resultado
            self.exibir_resultado(resultado)
            self.habilitar_botoes()
        else:
            self.agendamento_buscado = None
            self.reset_textos_labels()
            messagebox.showinfo("Não encontrado!", "Agendamento não encontrado.")

        self.limpar_campos()
        
    
    def habilitar_botoes(self):
        self.botao_atualizar.config(state='normal')
        self.botao_excluir.config(state='normal')
        
        
    def atualizar_agendamento(self):
        if self.agendamento_buscado:
            JanelaAtualizarAgendamento(self.janela, self.agendamento_buscado)
            self.frame.destroy()
        else:
            messagebox.showwarning("Aviso", "Nenhum agendamento selecionado.")

    
    
    def excluir_agendamento(self):
        if not self.agendamento_buscado:
            messagebox.showinfo("Erro", "Nenhum agendamento selecionado.")
            return
        tem_ctz = messagebox.askyesno("Tem certeza?", "Tem certeza de que deseja remover este agendamento?")
        
        if tem_ctz:
            resultado = maa.excluir_agendamento(self.agendamento_buscado.id)
            ut.exibir_mensagem(resultado, "Agendamento excluído com sucesso!", "Agendamento não encontrado.")
            self.frame.destroy()