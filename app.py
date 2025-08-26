from helpers.application import app, api
from helpers.CORS import cors

from helpers.database import db

from models.Pessoa import Pessoa
from models.Usuario import Usuario
from models.Nutricionista import Nutricionista
from models.Dieta import Dieta
from resources.UsuarioResource import UsuarioResource
from resources.NutricionistaResource import NutricionistaResource, NutricionistasResource
from resources.DietaResource import DietaResource

cors.init_app(app)

api.add_resource(UsuarioResource, '/usuarios')

api.add_resource(NutricionistaResource, '/nutricionistas')
api.add_resource(NutricionistasResource, '/nutricionistas/<int:id>')

api.add_resource(DietaResource, '/dietas')

with app.app_context():
    db.create_all()