from flask_restful import fields as flaskFields
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, ForeignKey

from app import db


dieta_fields ={
    "id": flaskFields.Integer,
    "nome_dieta": flaskFields.String,
    "calorias_diarias": flaskFields.String,
    "gerador": flaskFields.Nested({
        "id":flaskFields.Integer
    })
}

class Dieta(db.Model):
    __tablename__ = 'tb_dietas'

    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    nome_dieta: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    calorias_diarias:Mapped[float] = mapped_column(Float, nullable=False)
    
    # aponta pro ID da pessoa (usuario ou nutricionista) que a gerou
    gerador_id: Mapped[int]= mapped_column(Integer, ForeignKey('tb_pessoa.id'))

    gerador = relationship('Pessoa', back_populates='dietas_geradas')

    def __init__(self, nome_dieta:str, calorias_diarias:float, gerador_id:int):
        self.nome_dieta = nome_dieta
        self.calorias_diarias = calorias_diarias
        self.gerador_id = gerador_id
        
    
    def __repr__(self):
        return f'<Dieta {self.nome_dieta}>'