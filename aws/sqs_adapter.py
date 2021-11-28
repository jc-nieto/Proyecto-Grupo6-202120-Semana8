import boto3
from botocore.exceptions import ClientError
from config import APP_DEV, AWS_SESSION_TOKEN, AWS_SECRET_KEY, AWS_ACCESS_KEY, QUEUE_NAME

sqs = boto3.resource(
    'sqs',
    region_name='us-east-1'
)

if APP_DEV:
    sqs = boto3.resource(
        'sqs',
        region_name='us-east-1',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        aws_session_token=AWS_SESSION_TOKEN
    )


queue = sqs.get_queue_by_name(QueueName=QUEUE_NAME)
print('Connected to: {0}!'.format(queue.url))


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
