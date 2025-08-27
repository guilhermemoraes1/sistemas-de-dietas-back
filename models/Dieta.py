from flask_restful import fields as flaskFields
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, ForeignKey
from marshmallow import Schema, fields, validate

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
    gerador_id: Mapped[int]= mapped_column(Integer, ForeignKey('tb_pessoa.id', ondelete='CASCADE'))

    gerador = relationship('Pessoa', back_populates='dietas_geradas', passive_deletes=True)

    def __init__(self, nome_dieta:str, calorias_diarias:float, gerador_id:int):
        self.nome_dieta = nome_dieta
        self.calorias_diarias = calorias_diarias
        self.gerador_id = gerador_id
        
    
    def __repr__(self):
        return f'<Dieta {self.nome_dieta}>'


class PessoaMiniSchema(Schema):
    id = fields.Int()

class DietaSchema(Schema):
    id = fields.Int(dump_only=True)
    nome_dieta = fields.String(required=True, validate=validate.Length(min=2, max=100))
    calorias_diarias = fields.String(required=True)
    gerador_id = fields.Int(required=True, load_only=True)
    gerador = fields.Nested(PessoaMiniSchema, dump_only=True)
