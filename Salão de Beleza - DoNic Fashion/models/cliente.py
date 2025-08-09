class Cliente:
    def __init__(self, nome_cliente, cpf, telefone, email, agendamentos=None, id=None):
        self.nome_cliente = nome_cliente
        self.cpf = cpf
        self.telefone = telefone
        self.email = email
        self.agendamentos = agendamentos if agendamentos is not None else []
        self.id = id
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome_cliente': self.nome_cliente,
            'cpf': self.cpf,
            'telefone': self.telefone,
            'email': self.email,
            'agendamentos': self.agendamentos
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            nome_cliente=data.get('nome_cliente', ''),
            cpf=data.get('cpf', ''),
            telefone=data.get('telefone', ''),
            email=data.get('email', ''),
            agendamentos=data.get('agendamentos', []),
            id=data.get('id', None)
        )
    
    def __str__(self):
        return f"Cliente(id={self.id}, nome={self.nome_cliente}, cpf={self.cpf})"
    
    def __repr__(self):
        return self.__str__()