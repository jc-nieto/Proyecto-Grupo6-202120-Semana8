import os
from models import Tarea
from aws import *


def get_file(task):
    file_name = '{0}.{1}'.format(task.nombre, task.inputformat)
    download_file(file_name)


def convert_file(task):
    os.system('ffmpeg -i {} {}'.format(task.inputpath, task.outputpath))
    file_name = '{0}.{1}'.format(task.nombre, task.outputformat)
    upload_file(file_name)


def change_state(task):
    task: Tarea = Tarea.get_by_id(task.id)
    task.estado = 'processed'
    task.save()


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
        messages = receive_messages(10, 5)

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