import tkinter as tk
from janelas.avaliacao.janela_buscar_avaliacao import JanelaBuscaAvaliacao
from janelas.avaliacao.janela_cadastrar_avaliacao import JanelaCadastroAvaliacao
from janelas.agendamento.janela_buscar_agendamento import JanelaBuscaAgendamento
from janelas.agendamento.janela_cadastrar_agendamento import JanelaCadastroAgendamento
from janelas.cliente.janela_cadastrar_cliente import JanelaCadastroCliente


class JanelaPrincipal:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Salão de Beleza DoNIc Fashion")
        self.janela.iconbitmap("sistema.ico")
        self.centralizar_janela()

        self.menu_bar = tk.Menu(self.janela)
        self.janela.config(menu=self.menu_bar)

        menu_agendamentos = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Agendamento", menu=menu_agendamentos)
        menu_agendamentos.add_command(label="Cadastrar Agendamento", command=self.abrir_janela_cadastro_editora)
        menu_agendamentos.add_command(label="Buscar Agendamento", command=self.abrir_janela_busca_agendamento)
        menu_agendamentos.add_separator()
        menu_agendamentos.add_command(label="Sair", command=self.janela.quit)
        
        menu_avaliacoes = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Avaliação", menu=menu_avaliacoes)
        menu_avaliacoes.add_command(label="Buscar Avaliação", command=self.abrir_janela_busca_avaliacao)
        menu_avaliacoes.add_command(label="Cadastrar Avaliação", command=self.abrir_janela_cadastro_avaliacao)
        
        menu_clientes = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Cliente", menu=menu_clientes)
        menu_clientes.add_command(label="Cadastrar Cliente", command=self.abrir_janela_cadastro_cliente)

        self.janela.mainloop()


    def centralizar_janela(self):
        largura = 600
        altura = 500
        largura_tela = self.janela.winfo_screenwidth()
        altura_tela = self.janela.winfo_screenheight()

        x = (largura_tela // 2) - (largura // 2)
        y = (altura_tela // 2) - (altura // 2)

        self.janela.geometry(f"{largura}x{altura}+{x}+{y}")


    def limpar_widgets(self):
        if len(self.janela.winfo_children()) > 1:
            self.janela.winfo_children()[1].destroy()

    def abrir_janela_busca_avaliacao(self):
        self.limpar_widgets()
        JanelaBuscaAvaliacao(self.janela)

    def abrir_janela_cadastro_avaliacao(self):
        self.limpar_widgets()
        JanelaCadastroAvaliacao(self.janela)
        
    def abrir_janela_busca_agendamento(self):
        self.limpar_widgets()
        JanelaBuscaAgendamento(self.janela)

        
    def abrir_janela_cadastro_editora(self):
        self.limpar_widgets()
        JanelaCadastroAgendamento(self.janela)
        
        
    def abrir_janela_cadastro_cliente(self):
        self.limpar_widgets()
        JanelaCadastroCliente(self.janela)