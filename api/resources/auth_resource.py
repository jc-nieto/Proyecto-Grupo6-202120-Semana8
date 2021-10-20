from argon2.exceptions import VerifyMismatchError
from flask_restful import Resource
from flask import request
from sqlalchemy.exc import IntegrityError
from models import Usuario
from db import db
from flask_jwt_extended import jwt_required, create_access_token, get_jwt, get_jwt_identity, JWTManager
from helpers import encryptPassword, checkPassword
from marshmallow.exceptions import ValidationError

jwt = JWTManager()

class VistaSignIn(Resource):
    def post(self):
        try:
            nuevo_usuario = Usuario(nombre=request.json["nombre"],
                                    contrasena=encryptPassword(request.json["contrasena"]))
            db.session.add(nuevo_usuario)
            db.session.commit()
            token_de_acceso = create_access_token(identity=nuevo_usuario.id)
            return {"mensaje": "usuario creado exitosamente", "token": token_de_acceso}
        except IntegrityError as e:
            return {"mensaje": "Usuario ya Existe"}, 401


class VistaLogIn(Resource):
    def post(self):
        try:
            usuario = Usuario.query.filter(Usuario.nombre == request.json["nombre"]).first()
            if usuario is None:
                return {"mensaje": "El usuario no existe"}, 404
            else:
                checkPassword(usuario.contrasena, request.json["contrasena"])
                token_de_acceso = create_access_token(identity=usuario.id)
                return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso}
        except ValidationError as e:
            return {"mensaje": e.messages[0]}, 401
        except VerifyMismatchError as e:
            return {"mensaje": "Incorrect user or password"}, 404
