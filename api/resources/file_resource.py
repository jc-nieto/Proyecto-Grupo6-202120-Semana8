from flask_restful import Resource
from flask_jwt_extended import jwt_required,get_jwt_identity
from flask import send_file
from celery import Celery
from config import CELERY_RESULT_BACKEND, CELERY_BROKER_URL
import os
import subprocess

from models import Tarea
from common.error_handling import NotAllowed, NotReady, ObjectNotFound,NotAllowed

S3_NAME="filetransformer"
UPLOAD_DIRECTORY = "./data/input"
OUTPUT_DIRECTORY = "./data/output"

celery_app = Celery('tareas', broker=CELERY_BROKER_URL)

class FileResource(Resource):
    @jwt_required()
    def get(self,id_task,type):
        tarea:Tarea = Tarea.get_by_id(id_task)
        subprocess.call(['sudo','aws','s3','cp',f's3://{S3_NAME}/input/{tarea.nombre}.{tarea.inputformat}',f'{UPLOAD_DIRECTORY}/{tarea.nombre}.{tarea.inputformat}'])
        subprocess.call(['sudo','aws','s3','cp',f's3://{S3_NAME}/output/{tarea.nombre}.{tarea.outputformat}',f'{OUTPUT_DIRECTORY}/{tarea.nombre}.{tarea.outputformat}'])
        if tarea is None:
            raise ObjectNotFound
        if tarea.usuario_task != get_jwt_identity():
            raise NotAllowed('No tiene permisos para realizar ésta acción')
        if type =='input':
            path = tarea.inputpath.replace('./data','../data')
            celery_app.send_task('borrar_archivos', args=(tarea.id,), queue='procesar')
            return send_file(path)
        elif tarea.estado == 'processed' and type =='output':
            path = tarea.outputpath.replace('./data','../data')
            celery_app.send_task('borrar_archivos', args=(tarea.id,), queue='procesar')
            return send_file(path)
        else:
            raise NotReady('El archivo aún no esta listo')
