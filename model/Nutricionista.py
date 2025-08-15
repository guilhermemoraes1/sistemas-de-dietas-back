from app import db
from models.Pessoa import Pessoa
from models.Usuario import Usuario

class Nutricionista(Pessoa):
    __tablename__ = 'nutricionistas'
    
    crn = db.Column(db.String(20), unique=True, nullable=False)
    
    # Relacionamento de "um para muitos" com Usuario
    usuarios = db.relationship('Usuario', backref='nutricionista', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'nutricionista',
    }
    
    def __repr__(self):
        return f'<Nutricionista {self.nome}>'