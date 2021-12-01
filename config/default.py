from os import environ as env


PROPAGATE_EXCEPTIONS = True
JWT_SECRET_KEY = 'frase-secreta'

# Database configuration
SQLALCHEMY_TRACK_MODIFICATIONS = False
SHOW_SQLALCHEMY_LOG_MESSAGES = False
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}:{port}/{name}'.format(
    user=env.get('DB_USER', 'admin'),
    password=env.get('DB_PASSWORD', 'gerzonEsUnCrack'),
    host=env.get('DB_HOST', 'mydb.ccieufxfelfu.us-east-1.rds.amazonaws.com'),
    port=env.get('DB_PORT', '3306'),
    name=env.get('DB_NAME', 'myDB')
)

# AWS Credentials
AWS_ACCESS_KEY = env.get('AWS_ACCESS_KEY', 'ASIAXPWA7CPLZSVBBTTX')
AWS_SECRET_KEY = env.get('AWS_SECRET_KEY', '1TEZVXB4wFmH7J3FCjvnU1O9wwl0vK+TEUF12izc')
AWS_SESSION_TOKEN = env.get('AWS_SESSION_TOKEN', 'FwoGZXIvYXdzEP///////////wEaDJpablgf/huB7Q7zdSLLAWILG4HY3f7tMXESrmqkio2iU0jc1TxvbusNxaSp1IxJus1RcV828/MKtHGNPrjMNUQ9dF9ZOq35I164XJC6rf/XVipTJN343sYv46araKPqMElkhi3HlNpgHP5AXZTFP3a3jlXrnZn8vKE09wJsWXBcyMct6dLiiFRm768uEqMiLYr9rIn+yWU6t+Q8L4XxS2KCSRir1+U/6J+BWAiK91rJzg8isELsanrFaLIpOPGgCxfMEcI0BCtCWucLZ7fcIvOsRaLhhascyEjAKNuwjI0GMi2mu4zZjgRKWlD9M1/hN9L+Y7eRj+XbplAoWRwUVcmPwFaSfjpEROccmXClHQ8=')

# AWS - SQS & Bucket S3
QUEUE_NAME = env.get('AWS_QUEUE_NAME', 'consumers-queue.fifo')
S3_BUCKET_NAME = env.get('AWS_S3_BUCKET_NAME', 'filetransformer')

print('Settings:')
print('connection db: {0}'.format(SQLALCHEMY_DATABASE_URI))
print('Access key aws: {0}'.format(AWS_ACCESS_KEY))
print('Secret key aws: {0}'.format(AWS_SECRET_KEY))
print('Token session aws: {0}'.format(AWS_SESSION_TOKEN))
print('Queue name aws: {0}'.format(QUEUE_NAME))
print('Bucket name aws: {0}'.format(S3_BUCKET_NAME))
