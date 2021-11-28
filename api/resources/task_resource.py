from flask import request
from flask_restful import Resource
from uuid import uuid1
from typing import List
from flask_jwt_extended import get_jwt_identity, jwt_required
from werkzeug.datastructures import FileStorage
from common.error_handling import ObjectNotFound, NotAllowed
from models import Tarea, Usuario
from ..schemas import TareaSchema
import os
from aws import delete_file, upload_file, send_message


UPLOAD_DIRECTORY = "./data/input"
OUTPUT_DIRECTORY = "./data/output"
schema_task = TareaSchema()


def obtain_input_format(file):
    output_format = ''
    for char in reversed(file.filename):
        if char != '.':
            output_format += char
        else:
            break
    output_format = output_format[::-1]
    return output_format


class TaskResource(Resource):

    @jwt_required()
    def get(self, id_task):
        task: Tarea = Tarea.get_by_id(id_task)
        if task is None:
            raise ObjectNotFound('La tarea no existe')
        if task.usuario_task != get_jwt_identity():
            raise NotAllowed('No tiene permisos para realizar ésta acción')
        json = schema_task.dump(task)
        return json

    @jwt_required()
    def put(self, id_task):
        task: Tarea = Tarea.get_by_id(id_task)
        if task is None:
            raise ObjectNotFound('La tarea no existe')
        if task.usuario_task != get_jwt_identity():
            raise NotAllowed('No tiene permisos para realizar ésta acción')
        tasks: List[Tarea] = []
        if os.path.exists(task.outputpath):
            os.remove(task.outputpath)
        # Delete file.
        file_name = '{0}.{1}'.format(task.nombre, task.outputformat)
        delete_file(file_name)
        # os.system('/usr/local/bin/aws s3 rm s3://{}/output/{}.{}'.format(S3_NAME, tarea.nombre, tarea.outputformat))
        try:
            new_format = request.form.get('newFormat')
            output_path = os.path.join(
                OUTPUT_DIRECTORY, '{}.{}'.format(task.nombre, new_format))
            task.outputpath = output_path
            task.outputformat = new_format
            task.estado = 'uploaded'
            task.save()
            tasks.append(task)
            for task_item in tasks:
                send_message('process_task', task_item.id)
            return schema_task.dump(task)
        except Exception as e:
            print(e)

    @jwt_required()
    def delete(self, id_task):
        task: Tarea = Tarea.get_by_id(id_task)
        if task is None:
            raise ObjectNotFound('La tarea no existe')
        if task.usuario_task != get_jwt_identity():
            raise NotAllowed('No tiene permisos para realizar ésta acción')

        send_message('delete_task', task.id)
        if os.path.exists(task.inputpath):
            os.remove(task.inputpath)
        if os.path.exists(task.outputpath):
            os.remove(task.outputpath)

        return {'mensaje': 'La tarea fue borrada'}


class TaskListResource(Resource):

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user: Usuario = Usuario.get_by_id(user_id)
        if user is None:
            raise ObjectNotFound('El usuario no existe')

        tasks: List[Tarea] = user.tareas
        limit = request.args.get('max')
        order = request.args.get('order')

        if limit is not None:
            tasks = tasks[:int(limit)]

        if order is not None and int(order) == 0:
            tasks.sort(key=lambda x: x.id)
        elif order is not None and int(order) == 1:
            tasks.sort(key=lambda x: x.id, reverse=True)

        json = [schema_task.dump(task) for task in tasks]
        return json

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()

        user = Usuario.get_by_id(user_id)
        if user is None:
            raise ObjectNotFound('El usuario no existe')

        list_files = request.files.lists()
        files: List[FileStorage] = [elem[1] for elem in list_files][0]
        output_format = request.form.get('output_format')
        tasks: List[Tarea] = []

        for file in files:
            uuid = uuid1()
            input_format = obtain_input_format(file)
            input_path = os.path.join(UPLOAD_DIRECTORY, '{0}.{1}'.format(uuid, input_format))
            output_path = os.path.join(OUTPUT_DIRECTORY, '{0}.{1}'.format(uuid, output_format))
            file.save(input_path)
            file_name = '{0}.{1}'.format(uuid, input_format)
            upload_file(file_name, input_path, 'input')

            os.remove(input_path)
            task = Tarea(
                nombre='{}'.format(uuid),
                inputpath=input_path,
                outputpath=output_path,
                usuario_task=user_id,
                inputformat=input_format,
                outputformat=output_format
            )
            task.add()
            tasks.append(task)

        for item_task in tasks:
            send_message('process_task', item_task.id)

        return {'mensaje': 'La tarea fue creada con éxito'}
