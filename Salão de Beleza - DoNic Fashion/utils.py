from tkinter import messagebox


def exibir_mensagem(resultado, msg_sucesso, msg_erro):
    if resultado:
        messagebox.showinfo("Sucesso!", msg_sucesso)
    else:
        messagebox.showerror("Erro!", msg_erro)
        
        
def calcular_proximo_id(lista):
    ids = []
    if lista:
        for e in lista:
            ids.append(e.id)
    return max(ids, default=0) + 1