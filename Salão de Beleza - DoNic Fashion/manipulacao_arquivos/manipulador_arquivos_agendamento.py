import json
import os
from models.agendamento import Agendamento
import utils as ut

CAMINHO_ARQUIVO = "data/agendamento.json"


def inicializar_arquivo():
    try:
        diretorio = os.path.dirname(CAMINHO_ARQUIVO)
        if diretorio and not os.path.exists(diretorio):
            os.makedirs(diretorio)

        if not os.path.exists(CAMINHO_ARQUIVO):
            with open(CAMINHO_ARQUIVO, "w", encoding='utf-8') as f:
                json.dump([], f)
        return True
    except Exception as e:
        print(f"Erro ao inicializar arquivo de agendamentos: {e}")
        return False


def carregar_agendamentos():
    lista_agendamentos = []
    try:
        inicializar_arquivo()
        
        with open(CAMINHO_ARQUIVO, "r", encoding='utf-8') as f:
            conteudo = f.read().strip()
            if not conteudo:
                return lista_agendamentos
            
            agendamentos = json.loads(conteudo)
            
        # Garante que agendamentos é uma lista
        if not isinstance(agendamentos, list):
            print("Dados de agendamentos não são uma lista válida")
            return lista_agendamentos
            
        for a in agendamentos:
            try:
                # Usa **a para desempacotar o dicionário como argumentos
                obj_agendamento = Agendamento(**a)
                lista_agendamentos.append(obj_agendamento)
            except Exception as e:
                print(f"Erro ao converter agendamento: {e}")
                continue
                
        return lista_agendamentos
        
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON de agendamentos: {e}")
        return lista_agendamentos
    except Exception as e:
        print(f"Erro ao carregar agendamentos: {e}")
        return lista_agendamentos


def salvar_agendamentos(lista):
    try:
        inicializar_arquivo()
        
        if lista is None:
            lista = []
        
        dados = []
        for agendamento in lista:
            try:
                if hasattr(agendamento, 'to_dict'):
                    dados.append(agendamento.to_dict())
                else:
                    print(f"Agendamento sem método to_dict(): {agendamento}")
                    continue
            except Exception as e:
                print(f"Erro ao converter agendamento para dict: {e}")
                continue
        
        with open(CAMINHO_ARQUIVO, "w", encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
            
        return True
    except Exception as e:
        print(f"Erro ao salvar agendamentos: {e}")
        return False


def adicionar_agendamento(agendamento):
    try:
        # Carrega lista atual de agendamentos
        agendamentos = carregar_agendamentos()
        
        if agendamentos is None:
            agendamentos = []
        
        # Gera novo id
        try:
            proximo_id = ut.calcular_proximo_id(agendamentos)
        except Exception as e:
            print(f"Erro ao calcular próximo ID: {e}")
            proximo_id = len(agendamentos) + 1
        
        # Atribui novo id ao agendamento que quer inserir
        agendamento.id = proximo_id
            
        # Adiciona o novo agendamento na lista
        agendamentos.append(agendamento)
            
        # Salva a nova lista no arquivo
        resultado = salvar_agendamentos(agendamentos)
        if resultado:
            print(f"Agendamento adicionado com sucesso. ID: {agendamento.id}")
        
        return resultado
        
    except Exception as e:
        print(f"Erro ao adicionar agendamento: {e}")
        return False


def buscar_agendamento_por_id(id):
    """Busca agendamento por ID"""
    try:
        if isinstance(id, str):
            id = int(id)
            
        agendamentos = carregar_agendamentos()
        for agendamento in agendamentos:
            if hasattr(agendamento, 'id') and agendamento.id == id:        
                return agendamento
        return None
    except ValueError:
        print(f"Erro: ID inválido - {id}")
        return None
    except Exception as e:
        print(f"Erro ao buscar agendamento por ID: {e}")
        return None


def atualizar_agendamento(agendamento):
    try:
        agendamentos = carregar_agendamentos()
        
        if agendamentos is None:
            return False
            
        for idx, a in enumerate(agendamentos):
            if hasattr(a, 'id') and hasattr(agendamento, 'id') and a.id == agendamento.id:
                agendamentos[idx] = agendamento
                resultado = salvar_agendamentos(agendamentos)
                if resultado:
                    print(f"Agendamento ID {agendamento.id} atualizado com sucesso")
                return resultado
                
        print(f"Agendamento com ID {agendamento.id} não encontrado")
        return False
        
    except Exception as e:
        print(f"Erro ao atualizar agendamento: {e}")
        return False


def excluir_agendamento(id):
    try:
        agendamentos = carregar_agendamentos()
        
        if agendamentos is None:
            return False
            
        agendamentos_filtrados = []
        agendamento_removido = False
        
        for a in agendamentos:
            if hasattr(a, 'id') and a.id == id:
                agendamento_removido = True
                print(f"Agendamento ID {id} será removido")
            else:
                agendamentos_filtrados.append(a)
        
        if not agendamento_removido:
            print(f"Agendamento com ID {id} não encontrado")
            return False
            
        resultado = salvar_agendamentos(agendamentos_filtrados)
        if resultado:
            print(f"Agendamento ID {id} removido com sucesso")
            
        return resultado
        
    except Exception as e:
        print(f"Erro ao remover agendamento: {e}")
        return False