import os
import boto3
from botocore.exceptions import ClientError
from models import Tarea


aws_access_key = "ASIAZTRV6XHVA2X3HTMT"
aws_secret_key = "mXfNHkXLoXOFKAdS9InqoNY5PlI30uIDABBw2557"
aws_session_token = "FwoGZXIvYXdzEPT//////////wEaDARL/fK14T3j5eFwOCLMASDuyx/PPn1KfVGV+LKZBWKsBKK96prUfvLDmjykvMLUkp19TN4fguDy0brPzwzUGscCcjouhG7gnp4ZaZ0bqTnQa4CEZI6aB+QmPZ6+JuTHgZhNt5r4Q+2D51WF+COMco/ToiCaPuF3o1VBxRyWQNe25YP6sY1RQ4en+HSzeiJYlN+fo27o97rCqDNHovShXmXM/IYoSHZf9kh0buSVBL2XX0FL3wjz/Fty5DxKVMQ4CrcQwmn4nNBTF8omIqdjuAYhTLv/Eb8cKwyKaijG8YmNBjItL65/20gmz+Ll69xr8uCBHcOYzShBq0pKg4l2jWYhTgY7z5sOQZ50mxm1SX65"

# Get the service resource
sqs = boto3.resource(
    'sqs',
    region_name='us-east-1',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    aws_session_token=aws_session_token
)
'''
sqs = boto3.resource(
    'sqs',
    region_name='us-east-1'
)
'''
queue = sqs.get_queue_by_name(QueueName='consumers-queue.fifo')
print('Connected to: {0}!'.format(queue.url))

response = queue.send_message(
    MessageBody="1",
    MessageGroupId="process_task",
    MessageAttributes={'Task': {
        'StringValue': 'process_task',
        'DataType': 'String'
        }
    }
)


def delete_message(message):
    try:
        message.delete()
    except ClientError as error:
        print('Could not delete message: {0}'.format(message.message_id))
        raise error


def receive_messages(max_number, wait_time):
    try:
        messages = queue.receive_messages(
            MessageAttributeNames=['All'],
            MaxNumberOfMessages=max_number,
            WaitTimeSeconds=wait_time
        )
    except ClientError as error:
        print('Could not receive messages from queue: {0}'.format(queue))
        raise error
    else:
        return messages


def convert_file(task_id):
    task: Tarea = Tarea.get_by_id(task_id)
    if task is None:
        print('Task not exist')
        return
    os.system('ffmpeg -i {} {}'.format(task.inputpath, task.outputpath))


def change_state(task_id):
    task: Tarea = Tarea.get_by_id(task_id)
    if task is None:
        return
    task.estado = 'processed'
    task.save()


def process_task(message):
    convert_file(message)
    change_state(message)


def delete_task(message):
    task: Tarea = Tarea.get_by_id(message)
    if task is None:
        return
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

            if process == 'process_task':
                process_task(message.body)
            elif process == 'delete_task':
                delete_task(message.body)

            delete_message(message)


if __name__ == '__main__':
    process_messages()
