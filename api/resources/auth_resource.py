from __future__ import print_function

from argon2.exceptions import VerifyMismatchError
from flask_restful import Resource
from flask import request
from sqlalchemy.exc import IntegrityError
from models import Usuario
from db import db
from flask_jwt_extended import jwt_required, create_access_token, get_jwt, get_jwt_identity, JWTManager
from helpers import encryptPassword, checkPassword
from marshmallow.exceptions import ValidationError
from common.error_handling import ObjectNotFound, NotAllowed
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint

jwt = JWTManager()

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api_key'] = '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 '
api_instance = sib_api_v3_sdk.AccountApi(sib_api_v3_sdk.ApiClient(configuration))

api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
senderSmtp = sib_api_v3_sdk.SendSmtpEmailSender(name="test",email="dalt.rock@gmail.com")
sendTo = sib_api_v3_sdk.SendSmtpEmailTo(email="dalt.rock@gmail.com",name="Recipient Name")
arrTo = [sendTo] #Adding `to` in a list
send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(sender=senderSmtp,to=arrTo,html_content="This is a test",subject="This is a test subject") # SendSmtpEmail | Values to send a transactional email


class VistaSignIn(Resource):
    def post(self):
        try:
            if request.json["contrasena1"] != request.json["contrasena2"]:
                raise NotAllowed("Las contraseñas no coinciden")
            nuevo_usuario = Usuario(username=request.json["username"],
                                    contrasena=encryptPassword(request.json["contrasena1"]),
                                    email=request.json["email"])
            db.session.add(nuevo_usuario)
            db.session.commit()
            token_de_acceso = create_access_token(identity=nuevo_usuario.id)
            return {"mensaje": "usuario creado exitosamente", "token": token_de_acceso}
        except IntegrityError as e:
            return {"mensaje": "Usuario ya Existe"}, 401

    def put(self):
        try:
            # Send a transactional email
            api_response = api_instance.send_transac_email(send_smtp_email)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)

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
