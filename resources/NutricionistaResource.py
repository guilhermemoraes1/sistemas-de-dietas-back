from flask_restful import Resource
from flask import request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError, DataError

from helpers.logging import logger

from models.Nutricionista import Nutricionista, NutricionistaSchema
from helpers.database import db

nutricionista_schema = NutricionistaSchema() #cria um schema para um único objeto.
nutricionistas_schema = NutricionistaSchema(many=True) #cria um schema para uma lista (coleção) de objetos.

class NutricionistaResource(Resource):

    def get(self):
            logger.info("GET - Nutricionistas")
            nutricionistas = Nutricionista.query.all()
            return nutricionistas_schema.dump(nutricionistas), 200

    def post(self):
        logger.info("POST - Nutricionistas")
        data = request.get_json()

        try:
            validated = nutricionista_schema.load(data)
        except ValidationError as err:
            return {"errors": err.messages}, 400
        
        nutricionista = Nutricionista(**validated)
        db.session.add(nutricionista)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {"error": "Violação de integridade (email ou crn já existentes)."}, 409
        except DataError:
            db.session.rollback()
            return {"error": "Dados inválidos."}, 400
        
        return nutricionista_schema.dump(nutricionista), 201

class NutricionistasResource(Resource):
     
     def get(self, id):
        logger.info(f"GET por ID - Nutricionista id={id}")
        nutricionista = Nutricionista.query.get_or_404(id, description="Nutricionista não encontrado")
        return nutricionista_schema.dump(nutricionista), 200
     
     def put(self, id):
        logger.info(f"PUT - Nutricionista id={id}")
        nutricionista = Nutricionista.query.get_or_404(id, description="Nutricionista não encontrado")
        data = request.get_json()
        
        try:
            validated = nutricionista_schema.load(data)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        nutricionista.nome = validated["nome"]
        nutricionista.email = validated["email"]
        nutricionista.crn = validated["crn"]

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {"error": "Violação de integridade (email ou crn já existentes)."}, 409
        except DataError:
            db.session.rollback()
            return {"error": "Dados inválidos."}, 400

        return nutricionista_schema.dump(nutricionista), 200