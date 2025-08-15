from app import db
from models.Dieta import Dieta

class Pessoa(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    
    # Adiciona o relacionamento de um para muitos com a classe Dieta
    dietas_geradas = db.relationship('Dieta', backref='gerador', lazy=True)