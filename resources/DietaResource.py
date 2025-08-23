from flask_restful import Resource
from flask import request
from marshmallow import ValidationError

from models.Dieta import Dieta, DietaSchema
from helpers.database import db

dieta_schema = DietaSchema()
dietas_schema = DietaSchema(many=True)

class DietaResource(Resource):
    def get(self):
        dietas = Dieta.query.all()
        return dietas_schema.dump(dietas), 200

    def post(self):
        data = request.get_json()
        try:
            validated = dieta_schema.load(data)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        dieta = Dieta(**validated)
        db.session.add(dieta)
        db.session.commit()
        return dieta_schema.dump(dieta), 201
