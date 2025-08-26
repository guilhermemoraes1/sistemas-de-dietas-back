from flask_restful import Resource
from flask import request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError, DataError

from helpers.logging import logger

from models.Usuario import Usuario, UsuarioSchema
from helpers.database import db

usuario_schema = UsuarioSchema() #cria um schema para um único objeto.
usuarios_schema = UsuarioSchema(many=True) #cria um schema para uma lista (coleção) de objetos.

class UsuarioResource(Resource):
    def get(self):
        logger.info("GET - Usuarios")
        usuarios = Usuario.query.all()
        return usuarios_schema.dump(usuarios), 200

    def post(self):
        logger.info("POST - Usuarios")
        data = request.get_json()
        try:
            validated = usuario_schema.load(data)
        except ValidationError as err:
            return {"errors": err.messages}, 400
        
        usuario = Usuario(**validated)
        db.session.add(usuario)
        db.session.commit()
        return usuario_schema.dump(usuario), 201

class UsuariosResource(Resource):
    
    def get(self, id):
        logger.info(f"GET por ID - Usuario id={id}")
        usuario = Usuario.query.get_or_404(id, description="Usuário não encontrado")
        return usuario_schema.dump(usuario), 200
    
    def put(self, id):
        logger.info(f"PUT - Usuario id={id}")
        usuario = Usuario.query.get_or_404(id, description="Usuário não encontrado")
        data = request.get_json()

        try:
            validate = usuario_schema.load(data)
        except ValidationError as err:
            return {"errors": err.messages}, 400
        
        usuario.nome = validate["nome"]
        usuario.email = validate["email"]
        usuario.nutricionista_id = validate["nutricionista_id"]

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {"error": "Violação de integridade (email já existente ou nutricionista não existe)."}, 409
        except DataError:
            db.session.rollback()
            return {"error": "Dados inválidos."}, 400
        
        return usuario_schema.dump(usuario), 200