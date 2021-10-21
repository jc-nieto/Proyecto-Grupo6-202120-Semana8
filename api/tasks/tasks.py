from celery import Celery
import os

from models import Tarea

from config import CELERY_RESULT_BACKEND,CELERY_BROKER_URL

celery_app = Celery(
    'tareas',
    backend=CELERY_RESULT_BACKEND,
    broker=CELERY_BROKER_URL
)

def changeTaskState(task_id):
    task:Tarea = Tarea.get_by_id(task_id)
    task.estado = 'processed'
    task.save()


def convertFile(task_id):
    task:Tarea = Tarea.get_by_id(task_id)
    os.system('ffmpeg -i {} {}'.format(task.inputpath,task.outputpath))


@celery_app.task(name="procesar_tarea")
def cron(id_task):
    convertFile(id_task)
    changeTaskState(id_task)