from flask_restful import Resource
from flask_jwt_extended import jwt_required,get_jwt_identity
from flask import send_file
from celery import Celery
from config import CELERY_RESULT_BACKEND, CELERY_BROKER_URL, BROKER_TRANSPORT_OPTIONS
import os
import subprocess

from models import Tarea
from common.error_handling import NotAllowed, NotReady, ObjectNotFound,NotAllowed

S3_NAME="filetransformeraws4"

celery_app = Celery('tareas', broker=CELERY_BROKER_URL, broker_transport_options = BROKER_TRANSPORT_OPTIONS)

class FileResource(Resource):
    @jwt_required()
    def get(self,id_task,type):
        tarea:Tarea = Tarea.get_by_id(id_task)

        if tarea is None:
            raise ObjectNotFound
        if tarea.usuario_task != get_jwt_identity():
            raise NotAllowed('No tiene permisos para realizar ésta acción')
        if type =='input':
            os.system('/usr/local/bin/aws s3 cp s3://{}/input/{}.{} {}'.format(S3_NAME,tarea.nombre,tarea.inputformat,tarea.inputpath))
            path = tarea.inputpath
            file = send_file(os.path.abspath(path))
            os.remove(os.path.abspath(path))
            return file
        elif tarea.estado == 'processed' and type =='output':
            os.system('/usr/local/bin/aws s3 cp s3://{}/output/{}.{} {}'.format(S3_NAME,tarea.nombre,tarea.outputformat,tarea.outputpath))
            path = tarea.outputpath
            file = send_file(os.path.abspath(path))
            os.remove(os.path.abspath(path))
            return file
        else:
            raise NotReady('El archivo aún no esta listo')
