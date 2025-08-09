import json
import os
from models.cliente import Cliente
import utils as ut

CAMINHO_ARQUIVO = "data/cliente.json"


def garantir_diretorio_e_arquivo():
    try:
        diretorio = os.path.dirname(CAMINHO_ARQUIVO)
        if diretorio and not os.path.exists(diretorio):
            os.makedirs(diretorio)

        if not os.path.exists(CAMINHO_ARQUIVO):
            with open(CAMINHO_ARQUIVO, "w", encoding='utf-8') as f:
                json.dump([], f)
                
    except Exception as e:
        print(f"Erro ao garantir diretório e arquivo: {e}")


def carregar_clientes():
    lista_clientes = []
    try:
        garantir_diretorio_e_arquivo()
        
        with open(CAMINHO_ARQUIVO, "r", encoding='utf-8') as f:
            conteudo = f.read().strip()
            
            if not conteudo:
                return lista_clientes
            
            clientes = json.loads(conteudo)
            
            if not isinstance(clientes, list):
                print("Arquivo JSON não contém uma lista válida")
                return lista_clientes
            
            for c in clientes:
                try:
                    obj_cliente = Cliente.from_dict(c)
                    lista_clientes.append(obj_cliente)
                except Exception as e:
                    print(f"Erro ao converter cliente: {e}")
                    continue
                    
        return lista_clientes
        
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
        print("Arquivo JSON pode estar corrompido. Criando novo arquivo...")

        if os.path.exists(CAMINHO_ARQUIVO):
            backup_file = CAMINHO_ARQUIVO + ".backup"
            os.rename(CAMINHO_ARQUIVO, backup_file)
            print(f"Backup criado: {backup_file}")
        
        garantir_diretorio_e_arquivo()
        return lista_clientes
        
    except Exception as e:
        print(f"Erro ao carregar clientes: {e}")
        return lista_clientes
        
        
def salvar_clientes(lista):
    try:
        garantir_diretorio_e_arquivo()
        
        if lista is None:
            lista = []
        
        dados = []
        for cliente in lista:
            try:
                if hasattr(cliente, 'to_dict'):
                    dados.append(cliente.to_dict())
                else:
                    print(f"Cliente sem método to_dict(): {cliente}")
                    continue
            except Exception as e:
                print(f"Erro ao converter cliente para dict: {e}")
                continue
        
        with open(CAMINHO_ARQUIVO, "w", encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
            
        return True
        
    except Exception as e:
        print(f"Erro ao salvar clientes: {e}")
        return False


def adicionar_cliente(cliente):
    try:
        # Carrega lista atual de clientes
        clientes = carregar_clientes()
        
        # Garante que clientes é uma lista
        if clientes is None:
            clientes = []
        
        # Verifica se cliente já existe (por CPF, por exemplo)
        if hasattr(cliente, 'cpf'):
            for c in clientes:
                if hasattr(c, 'cpf') and c.cpf == cliente.cpf:
                    print(f"Cliente com CPF {cliente.cpf} já existe")
                    return False
        
        # Gera novo id
        try:
            proximo_id = ut.calcular_proximo_id(clientes)
            cliente.id = proximo_id
        except Exception as e:
            print(f"Erro ao calcular próximo ID: {e}")
            # Se não conseguir calcular ID, usa um valor simples
            cliente.id = len(clientes) + 1
            
        # Adiciona o novo cliente na lista
        clientes.append(cliente)
                
        # Salva a nova lista no arquivo
        resultado = salvar_clientes(clientes)
        
        if resultado:
            print(f"Cliente adicionado com sucesso. ID: {cliente.id}")
        
        return resultado
        
    except Exception as e:
        print(f"Erro ao adicionar cliente: {e}")
        return False
    
    
def buscar_cliente_por_id(id):  
    try:
        clientes = carregar_clientes()
        for c in clientes:
            if hasattr(c, 'id') and c.id == id:
                return c
        return None
    except Exception as e:
        print(f"Erro ao buscar cliente por ID: {e}")
        return None
    

def atualizar_cliente(cliente):
    try:
        clientes = carregar_clientes()
        
        if clientes is None:
            return False
            
        for idx, c in enumerate(clientes):
            if hasattr(c, 'id') and hasattr(cliente, 'id') and c.id == cliente.id:
                clientes[idx] = cliente
                resultado = salvar_clientes(clientes)
                if resultado:
                    print(f"Cliente ID {cliente.id} atualizado com sucesso")
                return resultado
                
        print(f"Cliente com ID {cliente.id} não encontrado")
        return False
        
    except Exception as e:
        print(f"Erro ao atualizar cliente: {e}")
        return False
    
    
def remover_cliente(id):
    try:
        clientes = carregar_clientes()
        
        if clientes is None:
            return False
            
        clientes_filtrados = []
        cliente_removido = False
        
        for c in clientes:
            if hasattr(c, 'id') and c.id == id:
                cliente_removido = True
                print(f"Cliente ID {id} será removido")
            else:
                clientes_filtrados.append(c)
        
        if not cliente_removido:
            print(f"Cliente com ID {id} não encontrado")
            return False
            
        resultado = salvar_clientes(clientes_filtrados)
        if resultado:
            print(f"Cliente ID {id} removido com sucesso")
            
        return resultado
        
    except Exception as e:
        print(f"Erro ao remover cliente: {e}")
        return False


def listar_todos_clientes():
    try:
        clientes = carregar_clientes()
        print(f"Total de clientes: {len(clientes)}")
        for cliente in clientes:
            if hasattr(cliente, 'nome_cliente') and hasattr(cliente, 'id'):
                print(f"ID: {cliente.id}, Nome: {cliente.nome_cliente}")
        return clientes
    except Exception as a:
        print(f"Erro ao listar clientes: {a}")
        return []