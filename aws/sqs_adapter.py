import boto3
from botocore.exceptions import ClientError


aws_access_key = "ASIAXPWA7CPLVIA5BSNI"
aws_secret_key = "cawKrL7FrWw/MR2k5LlB2q1HBS2mVmIld27Pnq9g"
aws_session_token = "FwoGZXIvYXdzEPz//////////wEaDOabvZUUM54geCMIGiLLAWv320101IhHihs7dRyAgG5w5D5tWhB+QW3KBE89qWrJ2Labh0gjMOc04sejHtbF7aki8N9hrOvxk3P4StaSGoK/+5yf6ghnBLSk+JUQ1y8EbdLJE2AnzgVvK5CGNIcCJVcbp1DPOBdOJ56yrD7oBNdDZ88ZfRTrijHemi+AukvffvrzBEPZ0DZ35CspTuhCbxZZwkLAX9oVYylnYUs64ldGmUkFHQ2zHsqxi4TvW+eM0E+qn3gI/cmL/RumAf8BIv/H1xaAUEyRm+PRKMzVi40GMi28V1xkTQKI+7H/N53ZjYCcI/cCxsftpqbqDQKuj6WEHA/lI4NMGw+Dopm659E="

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
