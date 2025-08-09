# Adicione estes métodos à sua classe Agendamento:

class Agendamento:
    def __init__(self, cliente, data, horario, servico, preco, duracao, profissional, status="Pendente", id=None):
        self.cliente = cliente
        self.data = data
        self.horario = horario
        self.servico = servico
        self.preco = preco
        self.duracao = duracao
        self.profissional = profissional
        self.status = status
        self.id = id
    
    def to_dict(self):
        return {
            'id': self.id,
            'cliente': self.cliente,
            'data': self.data,
            'horario': self.horario,
            'servico': self.servico,
            'preco': self.preco,
            'duracao': self.duracao,
            'profissional': self.profissional,
            'status': self.status
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            cliente=data.get('cliente', ''),
            data=data.get('data', ''),
            horario=data.get('horario', ''),
            servico=data.get('servico', ''),
            preco=data.get('preco', ''),
            duracao=data.get('duracao', ''),
            profissional=data.get('profissional', ''),
            status=data.get('status', 'Pendente'),
            id=data.get('id', None)
        )
    
    def __str__(self):
        return f"Agendamento(id={self.id}, cliente={self.cliente}, data={self.data}, servico={self.servico})"
    
    def __repr__(self):
        return self.__str__()