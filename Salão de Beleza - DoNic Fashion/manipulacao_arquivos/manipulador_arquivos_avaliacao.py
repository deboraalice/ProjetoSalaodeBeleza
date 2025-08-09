import json
import os
from models.avaliacao import Avaliacao
import utils as ut

CAMINHO_ARQUIVO = "data/avaliacao.json"


def carregar_avaliacoes():
    lista_avaliacoes = []
    try:
        if not os.path.exists(CAMINHO_ARQUIVO):
            # Cria o diretório se não existir
            os.makedirs(os.path.dirname(CAMINHO_ARQUIVO), exist_ok=True)
            return lista_avaliacoes
            
        with open(CAMINHO_ARQUIVO, "r", encoding='utf-8') as f:
            conteudo = f.read().strip()
            if not conteudo:
                return lista_avaliacoes
            
            avaliacoes = json.loads(conteudo)
            
            for av in avaliacoes:
                obj_avaliacao = Avaliacao.from_dict(av)
                lista_avaliacoes.append(obj_avaliacao)
        return lista_avaliacoes
    except FileNotFoundError:
        return lista_avaliacoes
    except json.JSONDecodeError:
        print(f"Erro ao decodificar JSON do arquivo {CAMINHO_ARQUIVO}")
        return lista_avaliacoes
    except Exception as e:
        print(f"Erro ao carregar avaliações: {e}")
        return lista_avaliacoes
        
        
def salvar_avaliacoes(lista):
    try:
        # Cria o diretório se não existir
        os.makedirs(os.path.dirname(CAMINHO_ARQUIVO), exist_ok=True)
        
        dados = [avaliacao.to_dict() for avaliacao in lista]
        
        with open(CAMINHO_ARQUIVO, "w", encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
            
        return True
    except Exception as e:
        print(f"Erro ao salvar avaliações: {e}")
        return False


def adicionar_avaliacao(avaliacao):
    try:
        # carrega avaliações existentes
        avaliacoes = carregar_avaliacoes()
        
        # gera novo id
        proximo_id = ut.calcular_proximo_id(avaliacoes)
        print(f"Próximo ID calculado: {proximo_id}")
        
        # atribui novo id à avaliação que quer inserir
        avaliacao.id_avaliacao = proximo_id
        avaliacao.id = proximo_id  # Garantindo que ambos sejam atualizados
        
        print(f"ID atribuído à avaliação: {avaliacao.id_avaliacao}")
            
        # adiciona a nova avaliação na lista
        avaliacoes.append(avaliacao)
                
        # salva a nova lista no arquivo
        resultado = salvar_avaliacoes(avaliacoes)
        print(f"Resultado do salvamento: {resultado}")
        
        return resultado, avaliacao
    except Exception as e:
        print(f"Erro ao adicionar avaliação: {e}")
        return False, None
    

def buscar_avaliacao_por_id(id_busca):  
    try:  
        avaliacoes = carregar_avaliacoes()
        print(f"Buscando ID {id_busca} entre {len(avaliacoes)} avaliações")
        
        for av in avaliacoes:
            # Verificar tanto id_avaliacao quanto id
            av_id_avaliacao = getattr(av, 'id_avaliacao', None)
            av_id = getattr(av, 'id', None)
            
            print(f"  Avaliação: id_avaliacao={av_id_avaliacao}, id={av_id}")
            
            # Comparar com ambos os possíveis IDs
            if av_id_avaliacao == id_busca or av_id == id_busca:
                print(f"Avaliação encontrada!")
                return av
                
        print("Avaliação não encontrada")
        return None
    except Exception as e:
        print(f"Erro ao buscar avaliação por ID: {e}")
        return None


def atualizar_avaliacao(avaliacao):
    try:
        avaliacoes = carregar_avaliacoes()
        for idx, av in enumerate(avaliacoes):
            if av.id == avaliacao.id:
                avaliacoes[idx] = avaliacao
                return salvar_avaliacoes(avaliacoes)
        return False
    except Exception as e:
        print(f"Erro ao atualizar avaliação: {e}")
        return False
    
    
def remover_avaliacao(id):
    try:
        avaliacoes = carregar_avaliacoes()
        novas_avaliacoes = []
        encontrou = False
        for av in avaliacoes:
            if av.id != id:
                novas_avaliacoes.append(av)
            else:
                encontrou = True
        
        if encontrou:
            return salvar_avaliacoes(novas_avaliacoes)
        else:
            return False
    except Exception as e:
        print(f"Erro ao remover avaliação: {e}")
        return False


def listar_avaliacoes():
    return carregar_avaliacoes()


def buscar_avaliacoes_por_cliente(id_cliente):
    try:
        avaliacoes = carregar_avaliacoes()
        avaliacoes_cliente = []
        for av in avaliacoes:
            if hasattr(av, 'id_cliente') and id_cliente in av.id_cliente:
                avaliacoes_cliente.append(av)
        return avaliacoes_cliente
    except Exception as e:
        print(f"Erro ao buscar avaliações por cliente: {e}")
        return []


def buscar_avaliacoes_por_agendamento(id_agendamento):
    try:
        avaliacoes = carregar_avaliacoes()
        avaliacoes_agendamento = []
        for av in avaliacoes:
            if hasattr(av, 'id_agendamento') and av.id_agendamento == id_agendamento:
                avaliacoes_agendamento.append(av)
        return avaliacoes_agendamento
    except Exception as e:
        print(f"Erro ao buscar avaliações por agendamento: {e}")
        return []