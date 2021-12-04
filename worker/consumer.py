import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from models import Tarea, Usuario
from aws import *


def get_file(task):
    file_name = '{0}.{1}'.format(task.nombre, task.inputformat)
    download_file(file_name, task.inputpath)


def convert_file(task):
    os.system('ffmpeg -i {} {}'.format(task.inputpath, task.outputpath))
    file_name = '{0}.{1}'.format(task.nombre, task.outputformat)
    upload_file(file_name, task.outputpath)


def change_state(task):
    usuario: Usuario=Usuario.get_by_id(task.id)
    task: Tarea = Tarea.get_by_id(task.usuario_task)
    task.estado = 'processed'
    task.save()
    message = Mail(
        from_email='jc.nieto@uniandes.edu.co',
        to_emails=usuario.email,
        subject='Archivo ID: {}'.format(task.id),
        html_content='<strong>El archivo solicitado ha sido procesado</strong>')
    try:
        sg = SendGridAPIClient(os.environ.get('APIKeyEmail'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)


def delete_local_files(task):
    os.remove(task.inputpath)
    os.remove(task.outputpath)


def process_task(task):
    get_file(task)
    convert_file(task)
    change_state(task)
    delete_local_files(task)


def delete_task(task):
    file_path = '{0}.{1}'.format(task.nombre, task.inputformat)
    delete_file('input/{0}'.format(file_path))
    delete_file('output/{0}'.format(file_path))
    task.delete()


def process_messages():
    more_messages = True

    while more_messages:
        messages = receive_messages(1, 20)

        for message in messages:
            if message.message_attributes is None:
                delete_message(message)
                continue

            print("Received message - Id: {0} Message {1}".format(message.message_id, message.body))
            process = message.message_attributes.get('Task').get('StringValue')

            task_id = message.body
            task: Tarea = Tarea.get_by_id(task_id)

            if task is None:
                print('Task not exist')
                delete_message(message)
                continue

            if process == 'process_task':
                process_task(task)
            elif process == 'delete_task':
                delete_task(task)

            delete_message(message)


if __name__ == '__main__':
    process_messages()
