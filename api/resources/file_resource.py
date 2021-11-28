from flask_restful import Resource
from flask_jwt_extended import jwt_required,get_jwt_identity
from flask import send_file
import os
from models import Tarea
from common.error_handling import NotReady, ObjectNotFound, NotAllowed
from aws import download_file


class FileResource(Resource):

    @jwt_required()
    def get(self, id_task, type_process):
        tarea: Tarea = Tarea.get_by_id(id_task)

        if tarea is None:
            raise ObjectNotFound
        if tarea.usuario_task != get_jwt_identity():
            raise NotAllowed('No tiene permisos para realizar ésta acción')

        file_name = '{0}.{1}'.format(tarea.nombre, tarea.inputformat)

        if type_process == 'input':
            path = tarea.inputpath
            download_file(file_name, path, type_process)

            file = send_file(os.path.abspath(path))
            os.remove(os.path.abspath(path))
            return file
        elif tarea.estado == 'processed' and type_process == 'output':
            path = tarea.outputpath
            download_file(file_name, path, type_process)

            file = send_file(os.path.abspath(path))
            os.remove(os.path.abspath(path))
            return file
        else:
            raise NotReady('El archivo aún no esta listo')
