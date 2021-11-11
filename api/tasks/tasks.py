from celery import Celery
import os
import smtplib, ssl
from db import db

port = 587  # For SSL

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
    os.system('ffmpeg -i {} {}'.format(task.inputpath, task.outputpath))
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


def deleteTask(task_id):
    task: Tarea = Tarea.get_by_id(task_id)
    task.delete()


@celery_app.task(name="procesar_tarea")
def cron(id_task):
    convertFile(id_task)
    changeTaskState(id_task)


@celery_app.task(name="borrar_tarea")
def delete(id_task):
    deleteTask(id_task)
