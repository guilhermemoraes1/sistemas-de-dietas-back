from flask_restful import fields as flaskFields
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String,ForeignKey


from models.Pessoa import Pessoa, pessoa_fields




nutricionista_fields={
    "id": flaskFields.Integer,
    "nome": flaskFields.String,
    "email": flaskFields.String,
    "crn": flaskFields.String,
    "usuarios": flaskFields.List(
        flaskFields.Nested({
        "id": flaskFields.Integer,
        "nome": flaskFields.String,
        "email": flaskFields.String
        })
    )}

class Nutricionista(Pessoa):
    __tablename__ = 'tb_nutricionistas'
    id: Mapped[int] = mapped_column(
        ForeignKey("tb_pessoa.id"), primary_key=True)
    crn :Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    
    # Relacionamento de "um para muitos" com Usuario
    usuarios = relationship('Usuario', back_populates='nutricionista', lazy=True, foreign_keys='Usuario.nutricionista_id' )

    __mapper_args__ = {
        'polymorphic_identity': 'nutricionista',
    }
    
    def __init__(self, nome, email, crn:str):
        super().__init__(nome, email)
        self.crn = crn

    def __repr__(self):
        return f'<Nutricionista {self.nome}>'