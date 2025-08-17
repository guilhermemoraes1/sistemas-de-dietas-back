from flask_restful import fields as flaskFields
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey


from models.Pessoa import Pessoa, pessoa_fields





usuario_fields = {
    "id": flaskFields.Integer,
    "nome": flaskFields.String,
    "email": flaskFields.String,
    "nutricionista": flaskFields.Nested({
        "crn":flaskFields.String
    })
}

class Usuario(Pessoa):
    __tablename__ = 'tb_usuarios'
    
    id: Mapped[int] = mapped_column(
        ForeignKey("tb_pessoa.id"), primary_key=True)
    # Relacionamento de "muitos para um" com Nutricionista
    nutricionista_id: Mapped[int]= mapped_column(Integer, ForeignKey('tb_nutricionistas.id'), nullable=True)
    
    nutricionista = relationship('Nutricionista', back_populates='usuarios', lazy=True, foreign_keys=[nutricionista_id])

    __mapper_args__ = {
        'polymorphic_identity': 'usuario',
    }
    

    def __init__(self, nome, email,nutricionista_id:int):
        super().__init__(nome, email)
        self.nutricionista_id = nutricionista_id

    def __repr__(self):
        return f'<Usuario {self.nome}>'