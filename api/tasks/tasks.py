from celery import Celery
import os
import smtplib, ssl
import db

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
    os.system('ffmpeg -i {} {}'.format(task.inputpath, task.outputpath))
    context = ssl.create_default_context()


def deleteTask(task_id):
    task: Tarea = Tarea.get_by_id(task_id)
    task.delete()


@celery_app.task(name="procesar_tarea")
def cron(id_task):
    tarea:Tarea = Tarea.get_by_id(id_task)
    convertFile(id_task)
    if os.path.exists(tarea.outputpath):
        os.remove(tarea.outputpath)
    changeTaskState(id_task)


@celery_app.task(name="borrar_tarea")
def delete(id_task):
    deleteTask(id_task)
