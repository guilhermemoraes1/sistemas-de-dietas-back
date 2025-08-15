from app import db

class Dieta(db.Model):
    __tablename__ = 'dietas'
    id = db.Column(db.Integer, primary_key=True)
    nome_dieta = db.Column(db.String(100), nullable=False)
    calorias_diarias = db.Column(db.Float, nullable=False)
    
    # aponta pro ID da pessoa (usuario ou nutricionista) que a gerou
    gerador_id = db.Column(db.Integer, db.ForeignKey('pessoas.id'), nullable=False)
    
    def __repr__(self):
        return f'<Dieta {self.nome_dieta}>'