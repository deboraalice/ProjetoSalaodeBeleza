import tkinter as tk
from tkinter import ttk, messagebox
import manipulacao_arquivos.manipulador_arquivos_avaliacao as maav
import manipulacao_arquivos.manipulador_arquivos_agendamento as maa
import manipulacao_arquivos.manipulador_arquivos_cliente as mac
import utils as ut
from models.avaliacao import Avaliacao


class JanelaCadastroAvaliacao:
    def __init__(self, janela):
        self.frame = tk.Frame(janela, width=420, height=350)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.notas_validas = [
            "0", "0.5", "1", "1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5"
        ]

        label_nota = tk.Label(self.frame, text="Nota: ")
        label_nota.grid(row=0, column=0, sticky='E', padx=5, pady=5)
        
        self.entrada_nota = ttk.Combobox(self.frame, values=self.notas_validas, state='readonly')
        self.entrada_nota.grid(row=0, column=1, sticky='W', padx=5, pady=5)
        self.entrada_nota.set("")

        label_comentario = tk.Label(self.frame, text="Comentário: ")
        label_comentario.grid(row=1, column=0, sticky='E', padx=5, pady=5)

        self.entrada_comentario = tk.Entry(self.frame)
        self.entrada_comentario.grid(row=1, column=1, sticky='W', padx=5, pady=5)
        
        label_cliente = tk.Label(self.frame, text="Cliente: ")
        label_cliente.grid(row=2, column=0, sticky='E', padx=5, pady=5)
        
        nomes_cliente = self.reset_cliente()
        
        self.listbox_cliente = tk.Listbox(self.frame, selectmode="extended", height=5)
        self.listbox_cliente.grid(row=2, column=1, sticky='W', padx=5, pady=5)
        for nome in nomes_cliente:
            self.listbox_cliente.insert(tk.END, nome)

        label_agendamento = tk.Label(self.frame, text="Agendamento: ")
        label_agendamento.grid(row=3, column=0, sticky='E', padx=5, pady=5)
        
        agendamento = self.reset_agendamento()
        
        self.combobox_agendamento = ttk.Combobox(self.frame, state="readonly", values=agendamento)
        self.combobox_agendamento.set("Selecione um agendamento")
        self.combobox_agendamento.grid(row=3, column=1, padx=5, pady=5)

        botao = tk.Button(self.frame, text="Salvar", command=self.cadastrar_avaliacao)
        botao.grid(row=4, column=0, padx=5, pady=5, columnspan=2)
        
        
    def recuperar_cliente_selecionado(self):
        item_selecionado = []
        indice_selecionado = self.listbox_cliente.curselection()
        if indice_selecionado:
            for indice in indice_selecionado:
                item = self.cliente[indice]
                if item:
                    item_selecionado.append(item.id)
        return item_selecionado
    
       
    def reset_cliente(self):
        self.cliente = mac.carregar_clientes()
        nomes_clientes = []
        
        for cliente in self.cliente:
            # Tentativa de descobrir o atributo correto do nome
            if hasattr(cliente, 'nome'):
                nomes_clientes.append(cliente.nome)
            elif hasattr(cliente, 'nome_cliente'):
                nomes_clientes.append(cliente.nome_cliente)
            elif hasattr(cliente, 'name'):
                nomes_clientes.append(cliente.name)
            else:
                # Se não encontrar, usa o ID como fallback
                nomes_clientes.append(f"Cliente ID: {getattr(cliente, 'id', 'N/A')}")
        
        return nomes_clientes
    
        
    def reset_agendamento(self):
        self.agendamento = maa.carregar_agendamentos()
        agendamento = [f"ID: {ag.id}" for ag in self.agendamento]
        return agendamento
        

    def limpar_campos(self):
        self.entrada_nota.set('')
        self.entrada_comentario.delete(0, 'end')
        self.listbox_cliente.delete(0, 'end')
        
        nomes_cliente = self.reset_cliente()
        for nome in nomes_cliente:
            self.listbox_cliente.insert(tk.END, nome)
        
        agendamento = self.reset_agendamento()
        self.combobox_agendamento.config(values=agendamento)
        self.combobox_agendamento.set("Selecione um agendamento")
        self.entrada_nota.focus()


    def cadastrar_avaliacao(self):
        # Validações
        nota = self.entrada_nota.get()
        if not nota:
            messagebox.showwarning("Atenção", "Selecione uma nota.")
            return
            
        comentario = self.entrada_comentario.get()
        if not comentario.strip():
            messagebox.showwarning("Atenção", "Digite um comentário.")
            return
            
        agendamento_selecionado = self.combobox_agendamento.current()
        if agendamento_selecionado == -1:
            messagebox.showwarning("Atenção", "Selecione um agendamento.")
            return
            
        agendamento = self.agendamento[agendamento_selecionado]
        
        id_cliente = self.recuperar_cliente_selecionado()
        
        if not id_cliente:
            messagebox.showwarning("Atenção", "Selecione pelo menos um Cliente.")
            return
        
        try:
            # cria objeto da classe Avaliacao
            avaliacao = Avaliacao(nota, comentario, agendamento.id, id_cliente)
            
            # envia o objeto para ser salvo no arquivo
            resultado, avaliacao = maav.adicionar_avaliacao(avaliacao)
            
            if resultado:
                for id_autor in id_cliente:
                    cliente = mac.buscar_cliente_por_id(id_autor)
                    if cliente:
                        if not hasattr(cliente, 'avaliacao') or cliente.avaliacao is None:
                            cliente.avaliacao = []
                        cliente.avaliacao.append(avaliacao.id_avaliacao)
                        mac.atualizar_cliente(cliente)
                
                # exibe mensagem de sucesso
                ut.exibir_mensagem(resultado, "Avaliação adicionada com sucesso!", "Erro ao adicionar avaliação.")
                self.limpar_campos()
            else:
                ut.exibir_mensagem(resultado, "Avaliação adicionada com sucesso!", "Erro ao adicionar avaliação.")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar avaliação: {str(e)}")