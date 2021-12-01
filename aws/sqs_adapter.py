import boto3
from config import AWS_SESSION_TOKEN, AWS_SECRET_KEY, AWS_ACCESS_KEY, QUEUE_NAME


sqs = boto3.resource(
    'sqs',
    region_name='us-east-1',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    aws_session_token=AWS_SESSION_TOKEN
)

queue = sqs.get_queue_by_name(QueueName=QUEUE_NAME)
print('Connected to: {0}!'.format(queue.url))


def send_message(process, message):
    queue.send_message(
        MessageBody=str(message),
        MessageGroupId=process,
        MessageAttributes={'Task': {
            'StringValue': process,
            'DataType': 'String'
            }
        }
    )
