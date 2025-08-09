from models.agendamento import Agendamento

class Avaliacao:
    def __init__(self, nota, comentarios, id_agendamento, id_cliente, id_avaliacao=None):
        self.nota = nota
        self.comentarios = comentarios
        self.id_agendamento = id_agendamento
        self.id_cliente = id_cliente
        self.id_avaliacao = id_avaliacao
        self.id = id_avaliacao
        
    def to_dict(self):
        return {
            'id_avaliacao': self.id_avaliacao,
            'id': self.id_avaliacao, 
            'nota': self.nota,
            'comentarios': self.comentarios,
            'id_agendamento': self.id_agendamento,
            'id_cliente': self.id_cliente
        }
    
    @classmethod
    def from_dict(cls, data):
        id_val = data.get('id_avaliacao') or data.get('id')
        
        avaliacao = cls(
            nota=data.get('nota'),
            comentarios=data.get('comentarios'),
            id_agendamento=data.get('id_agendamento'),
            id_cliente=data.get('id_cliente'),
            id_avaliacao=id_val
        )
        return avaliacao
    
    def __str__(self):
        return f"Avaliação {self.id_avaliacao}: Nota {self.nota} - {self.comentarios}"
    
    def __repr__(self):
        return f"Avaliacao(id={self.id_avaliacao}, nota={self.nota}, comentarios='{self.comentarios}', id_agendamento={self.id_agendamento}, id_cliente={self.id_cliente})"