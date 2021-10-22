from flask import request, send_file
from flask_restful import Resource
from werkzeug.datastructures import FileStorage
from uuid import uuid1
from typing import List
from flask_jwt_extended import get_jwt_identity, jwt_required

from common.error_handling import ObjectNotFound, NotAllowed
from models import Tarea, Usuario
from ..schemas import TareaSchema
from ..tasks import celery_app
import os

UPLOAD_DIRECTORY = "./data/input"
OUTPUT_DIRECTORY = "./data/output"

tarea_schema = TareaSchema()


def withoutPaths(tarea):
    inputpath, outputpath, rest = (lambda inputpath, outputpath, **rest: (inputpath, outputpath, rest))(**tarea)
    return rest


def obtainInputFormat(file):
    outputFormat = ''
    for char in reversed(file.filename):
        if char != '.':
            outputFormat += char
        else:
            break
    outputFormat = outputFormat[::-1]
    return outputFormat


class TaskResource(Resource):
    @jwt_required()
    def get(self, id_task):
        tarea: Tarea = Tarea.get_by_id(id_task)
        if tarea.usuario_task != get_jwt_identity():
            raise NotAllowed('No tiene permisos para realizar ésta acción')
        if tarea is None:
            raise ObjectNotFound('La tarea no existe')
        tareaJson = withoutPaths(tarea_schema.dump(tarea))
        return tareaJson

    def put(self, task_id):
        return 'TO DO'

    def delete(self, task_id):
        return 'TO DO'


class TaskListResource(Resource):

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()

        usuario: Usuario = Usuario.get_by_id(user_id)
        if usuario is None:
            raise ObjectNotFound('El usuario no existe')

        tareas: List[Tarea] = usuario.tareas
        limit = request.args.get('max')
        order = request.args.get('order')

        if limit is not None:
            tareas = tareas[:limit]

        if order is not None and order == 0:
            tareas.sort(key=lambda x: x.id)
        elif order is not None and order == 1:
            tareas.sort(key=lambda x: x.id, reverse=True)

        tareasJson = [withoutPaths(tarea_schema.dump(tarea)) for tarea in tareas]
        return tareasJson

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()

        usuario = Usuario.get_by_id(user_id)
        if usuario is None:
            raise ObjectNotFound('El usuario no existe')

        lista = request.files.lists()
        files: List[FileStorage] = [elem[1] for elem in lista][0]
        outputFormat = request.form.get('output_format')
        tasks: List[Tarea] = []

        for file in files:
            uuid = uuid1()
            inputFormat = obtainInputFormat(file)
            savePath = os.path.join(UPLOAD_DIRECTORY, '{}.{}'.format(uuid, inputFormat))
            outPath = os.path.join(OUTPUT_DIRECTORY, '{}.{}'.format(uuid, outputFormat))
            print(savePath, outPath)
            file.save(savePath)
            tarea = Tarea(nombre='{}'.format(uuid), inputpath=savePath, outputpath=outPath, usuario_task=user_id)
            tarea.add()
            tasks.append(tarea)

        for task in tasks:
            celery_app.send_task('procesar_tarea', args=(task.id,), queue='procesar')

        return {'mensaje': 'La tarea fue creada con éxito'}
