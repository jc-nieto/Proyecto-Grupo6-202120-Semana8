import boto3


# aws_access_key = "ASIAXPWA7CPLXDCARWEC"
# aws_secret_key = "1w3hgHlAqcSK42oMUFUBqihMvA0WnDy9tq+6OIG8"
# aws_session_token = "FwoGZXIvYXdzEPn//////////wEaDNFsYuGSG6OUYJVL7yLLAQzR8eeBTlxlzjwLnd8Ea7aHTm2uyhUMWCHdTgqxNJimeUe/tBLR5JYzQJ7HwS/3R2k3rh7k5ZPXzadg9A4dV/gjRM5zM8MrLXArd8x5qwJmTNKUDVVPrN3Mp4kGE6q0iAt2ib3cALyENrdLBL70WtU8sTzWC9mbhcfw6alT9aY5AxiBubfkarExCmPsrRiukRnm9rWLiP0rt2kXGLJMGedk5pNkiFEmrTjMJiMx4Z0s+EAHMmObpejPiz19ldIa/u3TAVibeA7Sn39tKL6Ii40GMi0DuWuvfctequN9CQSVdmSjwXdciqhocelCBhHzIB2qdw5or4eH40TpCfovvXQ="

# Get the service resource
'''
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

queue = sqs.get_queue_by_name(QueueName='consumers-queue.fifo')
