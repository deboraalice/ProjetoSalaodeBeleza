import tkinter as tk
import manipulacao_arquivos.manipulador_arquivos_avaliacao as maav
import manipulacao_arquivos.manipulador_arquivos_agendamento as maa
import manipulacao_arquivos.manipulador_arquivos_cliente as mac
from tkinter import messagebox
import utils as ut


class JanelaBuscaAvaliacao:
    def __init__(self, janela):
        self.janela = janela
        self.frame = tk.Frame(janela, width=420, height=350)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        self.avaliacao_buscada = None

        label_id_avaliacao = tk.Label(self.frame, text="ID: ")
        label_id_avaliacao.grid(row=0, column=0, sticky='E', padx=5, pady=5)

        self.entrada_id_avaliacao = tk.Entry(self.frame)
        self.entrada_id_avaliacao.grid(row=0, column=1, sticky='W', padx=5, pady=5)
        self.entrada_id_avaliacao.focus()

        self.botao = tk.Button(self.frame, text="Buscar", command=self.buscar_avaliacao)
        self.botao.grid(row=1, column=0, padx=5, pady=5, columnspan=2)

        self.label_nota_resultado = tk.Label(self.frame)
        self.label_nota_resultado.grid(row=2, column=0, sticky='W', padx=5, pady=5, columnspan=2)

        self.label_cliente_resultado = tk.Label(self.frame)
        self.label_cliente_resultado.grid(row=3, column=0, sticky='W', padx=5, pady=5, columnspan=2)

        self.label_comentario_resultado = tk.Label(self.frame)
        self.label_comentario_resultado.grid(row=4, column=0, sticky='W', padx=5, pady=5, columnspan=2)
        
        self.label_agendamento_resultado = tk.Label(self.frame)
        self.label_agendamento_resultado.grid(row=5, column=0, sticky='W', padx=5, pady=5, columnspan=2)
        
        self.botao_remover = tk.Button(self.frame, text="Remover", command=self.remover_avaliacao, state='disabled')
        self.botao_remover.grid(row=6, column=1, padx=5, pady=5, sticky='W')

        self.reset_textos_labels()


    def limpar_campos(self):
        self.entrada_id_avaliacao.delete(0, 'end')

    
    def reset_textos_labels(self):
        self.label_nota_resultado.config(text="Nota: ")
        self.label_cliente_resultado.config(text="Cliente: ")
        self.label_comentario_resultado.config(text="Comentário: ")
        self.label_agendamento_resultado.config(text="Agendamento: ")
    
    
    def exibir_resultado(self, resultado):
        self.reset_textos_labels()
        
        # Exibir nota
        texto_atual = self.label_nota_resultado.cget("text")
        texto_atual = texto_atual + str(resultado.nota)
        self.label_nota_resultado.config(text=texto_atual)
        
        # Exibir clientes
        texto_atual = self.label_cliente_resultado.cget("text")
        
        # Verificar se existe id_cliente e é uma lista
        if hasattr(resultado, 'id_cliente') and resultado.id_cliente:
            clientes_nomes = []
            for id_cliente in resultado.id_cliente:
                cliente = mac.buscar_cliente_por_id(id_cliente)
                if cliente:
                    # Tentar diferentes atributos para o nome
                    if hasattr(cliente, 'nome'):
                        clientes_nomes.append(cliente.nome)
                    elif hasattr(cliente, 'nome_cliente'):
                        clientes_nomes.append(cliente.nome_cliente)
                    elif hasattr(cliente, 'name'):
                        clientes_nomes.append(cliente.name)
                    else:
                        clientes_nomes.append(f"Cliente ID: {id_cliente}")
                else:
                    clientes_nomes.append(f"Cliente ID: {id_cliente} (não encontrado)")
            
            texto_atual = texto_atual + ", ".join(clientes_nomes)
        else:
            texto_atual = texto_atual + "Nenhum cliente associado"
            
        self.label_cliente_resultado.config(text=texto_atual)
        
        # Exibir comentário
        texto_atual = self.label_comentario_resultado.cget("text")
        comentario = getattr(resultado, 'comentarios', '') or getattr(resultado, 'comentario', '')
        texto_atual = texto_atual + str(comentario)
        self.label_comentario_resultado.config(text=texto_atual)
        
        # Exibir agendamento
        texto_atual = self.label_agendamento_resultado.cget("text")
        try:
            # Buscar agendamento pelo ID
            agendamento = maa.buscar_agendamento_por_id(resultado.id_agendamento)
            if agendamento:
                # Tentar mostrar informações relevantes do agendamento
                if hasattr(agendamento, 'data') and hasattr(agendamento, 'hora'):
                    texto_atual = texto_atual + f"ID: {resultado.id_agendamento} - {agendamento.data} às {agendamento.hora}"
                else:
                    texto_atual = texto_atual + f"ID: {resultado.id_agendamento}"
            else:
                texto_atual = texto_atual + f"ID: {resultado.id_agendamento} (não encontrado)"
        except Exception as e:
            texto_atual = texto_atual + f"ID: {resultado.id_agendamento} (erro ao buscar)"
            
        self.label_agendamento_resultado.config(text=texto_atual)
    
    
    def buscar_avaliacao(self):
        try:
            # Pegar o ID digitado
            id_texto = self.entrada_id_avaliacao.get().strip()
            
            if not id_texto:
                messagebox.showwarning("Atenção", "Digite um ID para buscar.")
                return
                
            # Converter para inteiro
            id_avaliacao = int(id_texto)
            
            # Debug: verificar se existem avaliações no arquivo
            todas_avaliacoes = maav.carregar_avaliacoes()
            print(f"Total de avaliações carregadas: {len(todas_avaliacoes)}")
            
            if todas_avaliacoes:
                print("IDs disponíveis:")
                for av in todas_avaliacoes:
                    print(f"  - ID: {getattr(av, 'id_avaliacao', 'N/A')} ou {getattr(av, 'id', 'N/A')}")
            
            # Buscar a avaliação
            resultado = maav.buscar_avaliacao_por_id(id_avaliacao)
            print(f"Resultado da busca para ID {id_avaliacao}: {resultado}")
            
            if resultado:
                self.avaliacao_buscada = resultado
                self.exibir_resultado(resultado)
                self.habilitar_botoes()
            else:
                self.avaliacao_buscada = None
                self.reset_textos_labels()
                messagebox.showinfo("Não encontrada!", f"Avaliação com ID {id_avaliacao} não encontrada.\n\nVerifique se o ID existe.")
                self.botao_remover.config(state='disabled')

            self.limpar_campos()
            
        except ValueError:
            messagebox.showerror("Erro", "O ID deve ser um número válido.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar avaliação: {str(e)}")
            print(f"Erro detalhado: {e}")
        
    
    def habilitar_botoes(self):
        self.botao_remover.config(state='normal')
        
    
    def remover_avaliacao(self):
        if not self.avaliacao_buscada:
            messagebox.showwarning("Atenção", "Nenhuma avaliação selecionada para remover.")
            return
            
        # pergunta se quer remover
        tem_ctz = messagebox.askyesno("Tem certeza?", "Tem certeza de que deseja remover esta avaliação?")
        
        if tem_ctz:
            try:
                # Remover a avaliação
                resultado = maav.remover_avaliacao(self.avaliacao_buscada.id_avaliacao)
                
                # exibe mensagem de sucesso ou falha
                ut.exibir_mensagem(resultado, "Avaliação removida com sucesso!", "Erro ao remover avaliação.")
                
                if resultado:
                    # Limpar os campos e desabilitar botão
                    self.reset_textos_labels()
                    self.botao_remover.config(state='disabled')
                    self.avaliacao_buscada = None
                    
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao remover avaliação: {str(e)}")
