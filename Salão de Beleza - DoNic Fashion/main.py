import tkinter as tk
from tkinter import messagebox
from janela_principal import JanelaPrincipal

class LoginWindow:
    def __init__(self):
        self.USERNAME = "admin"
        self.PASSWORD = "admin"
        
        self.janela = tk.Tk()
        self.janela.title("Login")
        self.janela.geometry("600x500")
        self.janela.resizable(False, False)
        self.janela.iconbitmap("sistema.ico")
        
        self.create_widgets()
        
    def create_widgets(self):
        tk.Label(self.janela, text="Usuário:").pack(pady=10)

        self.user_entry = tk.Entry(self.janela)
        self.user_entry.pack(pady=5)
        self.user_entry.focus()

        tk.Label(self.janela, text="Senha:").pack(pady=10)

        self.pass_entry = tk.Entry(self.janela, show="*")
        self.pass_entry.pack(pady=5)

        tk.Button(self.janela, text="Entrar", command=self.validate_login).pack(pady=15)

        self.janela.bind('<Return>', lambda event: self.validate_login())
        
    def validate_login(self):
        username = self.user_entry.get()
        password = self.pass_entry.get()
        
        if username == self.USERNAME and password == self.PASSWORD:
            self.janela.destroy()
            JanelaPrincipal()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos!")
            self.user_entry.delete(0, tk.END)
            self.pass_entry.delete(0, tk.END)

    def run(self):
        self.janela.mainloop()


if __name__ == "__main__":
    login = LoginWindow()
    login.run()
