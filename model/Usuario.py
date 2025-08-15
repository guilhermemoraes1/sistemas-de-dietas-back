from app import db
from models.Pessoa import Pessoa

class Usuario(Pessoa):
    __tablename__ = 'usuarios'
    
    # Relacionamento de "muitos para um" com Nutricionista
    nutricionista_id = db.Column(db.Integer, db.ForeignKey('nutricionistas.id'), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'usuario',
    }

    def __repr__(self):
        return f'<Usuario {self.nome}>'