from flask_restful import fields as flaskFields
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer


from app import db


pessoa_fields ={
    "id": flaskFields.Integer,
    "nome": flaskFields.String,
    "email": flaskFields.String
}

class Pessoa(db.Model):
    # __abstract__ = True
    __tablename__ = 'tb_pessoa'
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    nome: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    tipo: Mapped[str] = mapped_column(String(50))

    
    __mapper_args__ = {
        "polymorphic_identity": "pessoa",
        "polymorphic_on": "tipo",
    }
    # Adiciona o relacionamento de um para muitos com a classe Dieta
    dietas_geradas = relationship('Dieta', back_populates='gerador', lazy=True, passive_deletes=True)

    def __init__(self, nome:str, email:str):
        self.nome = nome
        self.email = email
        



