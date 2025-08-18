from flask_restful import Resource
from flask import request
from models.Usuario import Usuario, UsuarioSchema
from helpers.database import db

usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)

class UsuarioResource(Resource):
    def get(self):
        usuarios = Usuario.query.all()
        return usuarios_schema.dump(usuarios), 200

    def post(self):
        data = request.get_json()
        try:
            validated = usuario_schema.load(data)
        except ValidationError as err:
            return {"errors": err.messages}, 400
        
        usuario = Usuario(**validated)
        db.session.add(usuario)
        db.session.commit()
        return usuario_schema.dump(usuario), 201
