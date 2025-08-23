from flask_restful import Resource
from flask import request
from marshmallow import ValidationError

from models.Nutricionista import Nutricionista, NutricionistaSchema
from helpers.database import db

nutricionista_schema = NutricionistaSchema()
nutricionistas_schema = NutricionistaSchema(many=True)

class NutricionistaResource(Resource):
    def get(self):
        nutricionistas = Nutricionista.query.all()
        return nutricionistas_schema.dump(nutricionistas), 200

    def post(self):
        data = request.get_json()
        try:
            validated = nutricionista_schema.load(data)
        except ValidationError as err:
            return {"errors": err.messages}, 400
        
        nutricionista = Nutricionista(**validated)
        db.session.add(nutricionista)
        db.session.commit()
        return nutricionista_schema.dump(nutricionista), 201
