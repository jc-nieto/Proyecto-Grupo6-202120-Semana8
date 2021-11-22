from celery import Celery
import os
import subprocess
import smtplib, ssl
from db import db
from time import sleep

port = 587  # For SSL

S3_NAME="filetransformers3"

from models import Tarea, Usuario

from config import CELERY_RESULT_BACKEND, CELERY_BROKER_URL

celery_app = Celery(
    'tareas',
    backend=CELERY_RESULT_BACKEND,
    broker=CELERY_RESULT_BACKEND
)


def changeTaskState(task_id):
    task: Tarea = Tarea.get_by_id(task_id)
    task.estado = 'processed'
    task.save()


def convertFile(task_id):
    task: Tarea = Tarea.get_by_id(task_id)
    usuario: Usuario = Usuario.get_by_id(task.usuario_task)
    try:
        os.system('ffmpeg -i {} {}'.format(task.inputpath, task.outputpath))
        os.system('/usr/local/bin/aws s3 cp {} s3://{}/output/{}.{}'.format(task.outputpath,S3_NAME,task.nombre,task.outputformat))
        context = ssl.create_default_context()
        
        with smtplib.SMTP("smtp.sendgrid.net", port) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login("apikey", password='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')
            subject = 'Prueba'
            body = 'Su archivo ha sido procesado'
            msg = f'From:daniel@crecyservices.io\nSubject:{subject}\n\n{body}'
            server.sendmail("daniel@crecyservices.io", usuario.email, msg)
    except:
        pass

def download_input_file(task_id):
    task: Tarea = Tarea.get_by_id(task_id)
    os.system('/usr/local/bin/aws s3 cp s3://{}/input/{}.{} {}'.format(S3_NAME,task.nombre,task.inputformat,task.inputpath))


def deleteTask(task_id):
    task: Tarea = Tarea.get_by_id(task_id)
    delete_bucket_files(task)
    task.delete()

def delete_bucket_files(task: Tarea):
    os.system('/usr/local/bin/aws s3 rm s3://{}/input/{}.{}'.format(S3_NAME,task.nombre,task.inputformat))
    os.system('/usr/local/bin/aws s3 rm s3://{}/output/{}.{}'.format(S3_NAME,task.nombre,task.outputformat))

def delete_files(task_id):
    task: Tarea = Tarea.get_by_id(task_id)
    os.remove(task.inputpath)
    os.remove(task.outputpath)


@celery_app.task(name="procesar_tarea")
def cron(id_task):
    download_input_file(id_task)
    convertFile(id_task)
    changeTaskState(id_task)
    delete_files(id_task)

@celery_app.task(name="borrar_archivos")
def borrar_archivos(id_task):
    sleep(5)
    delete_files(id_task)


@celery_app.task(name="borrar_tarea")
def delete(id_task):
    deleteTask(id_task)
