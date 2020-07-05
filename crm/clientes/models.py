from crm import app, db
from datetime import datetime

class Cliente(db.Model):
    __tablename__ = "cliente"

    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(30))
    historico_status = db.Column(db.String(100))
    observacoes = db.Column(db.String)
    email = db.Column(db.String)
    telefone = db.Column(db.Integer)
    endereco = db.Column(db.String)
    status = db.Column(db.String)
    datainsercao = db.Column(db.String)
    prospeccao = db.Column(db.String)

    def __init__(self, nome, email,telefone, endereco, status, datainsercao, prospeccao):
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.endereco = endereco
        self.status = status
        self.datainsercao = datainsercao
        self.prospeccao = prospeccao
        self.historico_status = "--------,--------,--------,--------,--------,--------"
        self.observacoes = "Sem comentarios Ainda!"
