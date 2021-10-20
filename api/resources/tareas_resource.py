from typing import List
from flask_restful import Resource
from flask import request, send_file, current_app, Flask
from celery import Celery
from werkzeug.datastructures import FileStorage
from uuid import uuid1
from flask_jwt_extended import jwt_required, create_access_token, get_jwt, get_jwt_identity, JWTManager

import config.default
from models import Tarea
from ..schemas import TareaSchema
from db import db
import os

UPLOAD_DIRECTORY = "../data/input"
OUTPUT_DIRECTORY = "../data/output"

def withoutPaths(tarea):
    inputpath, outputpath, rest = (lambda inputpath, outputpath, **rest: (inputpath, outputpath, rest))(**tarea)
    return rest


celery_app = Celery(
    "tareas",
    broker=f'' + config.default.REDIS_SERVER,
    backend=f'' + config.default.REDIS_SERVER,
)

tarea_schema = TareaSchema()


class TareasView(Resource):
    @jwt_required()
    def post(self):
        lista = request.files.lists()
        usuario = get_jwt_identity()
        print(usuario)
        files: List[FileStorage] = [elem[1] for elem in lista][0]
        outputFormat = request.form.get('output_format')
        inputFormat = request.form.get('input_format')
        tasks: List[Tarea] = []
        for file in files:
            uuid = uuid1()
            savePath = os.path.join(UPLOAD_DIRECTORY, '{}.{}'.format(uuid, inputFormat))
            outPath = os.path.join(OUTPUT_DIRECTORY, '{}.{}'.format(uuid, outputFormat))
            file.save(savePath)
            tarea = Tarea(nombre='{}'.format(uuid), inputpath=savePath, outputpath=outPath, usuario=usuario)
            db.session.add(tarea)
            tasks.append(tarea)
        db.session.commit()
        for task in tasks:
            celery_app.send_task('procesar_tarea', args=(task.id,), queue='prueba1')

        return {'mensaje': 'La tarea fue creada con éxito'}

    def get(self):
        tareas = Tarea.query.all()
        tareasJson = [withoutPaths(tarea_schema.dump(tarea)) for tarea in tareas]

        return tareasJson


class TareaView(Resource):

    def get(self, id_task):
        tarea = Tarea.query.get_or_404(id_task)
        tareaJson = withoutPaths(tarea_schema.dump(tarea))
        return tareaJson


class FileView(Resource):

    def get(self, id_task):
        tarea = Tarea.query.get_or_404(id_task)
        if tarea.estado == 'processed':
            return send_file(tarea.outputpath)
        else:
            return {'mensaje': 'El archivo aún no esta listo'}, 400
