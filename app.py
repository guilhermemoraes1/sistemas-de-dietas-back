from helpers.application import app, api
from helpers.CORS import cors

from helpers.database import db

from models.Pessoa import Pessoa
from models.Usuario import Usuario
from models.Nutricionista import Nutricionista
from models.Dieta import Dieta
cors.init_app(app)



with app.app_context():
    db.create_all()