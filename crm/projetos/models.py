from crm import app, db
from datetime import datetime

class Projeto(db.Model):
    __tablename__ = "projeto"

    id = db.Column(db.Integer, primary_key = True)
    nome        = db.Column(db.String,nullable = False)
    comentarios = db.Column(db.String, nullable = True)
    tipo        = db.Column(db.String)
    cliente     = db.Column(db.String)    
    url         = db.Column(db.String)
    valor       = db.Column(db.Integer)
    po          = db.Column(db.String)
    prazo       = db.Column(db.Integer)
    inicio      = db.Column(db.String)
    data        = db.Column(db.Integer)
    status      = db.Column(db.String)
    nota        = db.Column(db.Integer)

    def __init__(self, nome,tipo,cliente,url,valor,po, prazo, inicio, status):
        self.nome = nome
        self.tipo = tipo
        self.cliente = cliente
        self.url = url  
        self.valor = valor
        self.po = po
        self.prazo = prazo
        self.data = prazo
        self.inicio = inicio
        self.status = status
        self.comentarios = "Sem comentarios Ainda!"
        self.nota = -1

        teste = self.prazo.split('-')
        teste = teste[0] + teste[1] + teste[2]
        self.prazo = int(teste)
        self.data = int(teste)
       
        self.prazo = str(self.prazo)
        self.prazo = self.prazo[6] + self.prazo[7] + '/' + self.prazo[4] + self.prazo[5] + '/' + self.prazo[0] + self.prazo[1] + self.prazo[2] + self.prazo[3]
        
        testee = self.inicio.split('-')
        testee = testee[0] + testee[1] + testee[2]
        self.inicio = int(testee)
        
        self.inicio = str(self.inicio)
        self.inicio = self.inicio[6] + self.inicio[7] + '/' + self.inicio[4] + self.inicio[5] + '/' + self.inicio[0] + self.inicio[1] + self.inicio[2] + self.inicio[3]

class Nota(db.Model):
    __tablename__ = "nota"

    id      = db.Column(db.Integer, primary_key = True)
    nota    = db.Column(db.Integer)

    def __init__(self, nota):
        self.nota = nota
