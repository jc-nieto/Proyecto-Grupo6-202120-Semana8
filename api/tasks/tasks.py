from celery import Celery
import os
import subprocess
import smtplib, ssl
from db import db
from time import sleep

port = 587  # For SSL

S3_NAME="filetransformer"
UPLOAD_DIRECTORY = "./data/input"
OUTPUT_DIRECTORY = "./data/output"

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
        subprocess.call(['ffmpeg','-i',f'{task.inputpath}',f'{task.outputpath}'])
        subprocess.call(['aws','s3','cp',f'{task.outputpath}',f's3://{S3_NAME}/output/{task.nombre}.{task.inputformat}'])
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
    subprocess.call(['aws','s3','cp',f's3://{S3_NAME}/input/{task.nombre}.{task.inputformat}',f'{UPLOAD_DIRECTORY}/{task.nombre}.{task.inputformat}'])

def deleteTask(task_id):
    task: Tarea = Tarea.get_by_id(task_id)
    delete_bucket_files(task)
    task.delete()

def delete_bucket_files(task: Tarea):
    subprocess.call(['aws','s3','rm',f's3://{S3_NAME}/input/{task.nombre}.{task.inputformat}'])
    subprocess.call(['aws','s3','rm',f's3://{S3_NAME}/output/{task.nombre}.{task.outputformat}'])

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
