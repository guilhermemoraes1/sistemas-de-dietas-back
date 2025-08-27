from flask_restful import Resource
from flask import request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError, DataError

from helpers.logging import logger

from models.Dieta import Dieta, DietaSchema
from helpers.database import db

dieta_schema = DietaSchema()
dietas_schema = DietaSchema(many=True)

class DietaResource(Resource):
    def get(self):
        logger.info("GET - Dietas")
        dietas = Dieta.query.all()
        return dietas_schema.dump(dietas), 200

    def post(self):
        logger.info("POST - Dietas")
        data = request.get_json()
        try:
            validated = dieta_schema.load(data)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        dieta = Dieta(**validated)
        db.session.add(dieta)
        db.session.commit()
        return dieta_schema.dump(dieta), 201

class DietasResource(Resource):
    
    def get(self, id):
        logger.info(f"GET por ID - Dieta id={id}")
        dieta = Dieta.query.get_or_404(id, description="Dieta não encontrada")
        return dieta_schema.dump(dieta), 200
    
    def put(self, id):
        logger.info(f"PUT - Dieta id={id}")
        dieta = Dieta.query.get_or_404(id, description="Dieta não encontrada")
        data = request.get_json()

        if "gerador_id" in data:
            return {"error": "gerador_id não pode ser alterado."}, 400
        
        try:
            validated = dieta_schema.load(data, partial=("gerador_id",))
        except ValidationError as err:
            return {"errors": err.messages}, 400
        
        dieta.nome_dieta = validated["nome_dieta"]
        dieta.calorias_diarias = validated["calorias_diarias"]

        try:
            db.session.commit()
        except DataError:
            db.session.rollback()
            return {"error": "Dados inválidos."}, 400

        return dieta_schema.dump(dieta), 200

