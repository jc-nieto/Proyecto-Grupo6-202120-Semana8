from os import environ as env


PROPAGATE_EXCEPTIONS = True

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
AWS_SESSION_TOKEN = env.get('AWS_SESSION_TOKEN', 'FwoGZXIvYXdzEAYaDD6MlsVx+pliA3+fiyLLAWzsbgKkIcPKCtswICH5G2wrTFubut3ajMpAcvy4XwbbBAO6gfibeJPxZvZRYMCRKBsTC1h52/Q+vCLkruwEw+TJZmkalAezd55TZxFjBKEcRXZNhqqJJlpesXNVfD9sRwGDL/4vupGC3a4E/E74F1tDQJGJLDUG0pN2Npp/tpKGZUbRFOuhBZ223HPQsgygc+rJm63j9zx4bL1ZmZ2Y6qDbU1s5IGx5ryt+rIzSTm0c5s/dZXNH2BTrc86LGWSgsKZZzMlOY/CadX3tKO/3jY0GMi2c2S2HDbjjntuzotc4kOaQ3CIv12rsdfF3+gh3Z9GAwKJzSY6C0m4dhB8XGXQ=')

# AWS - SQS & Bucket S3
QUEUE_NAME = env.get('AWS_QUEUE_NAME', 'consumers-queue.fifo')
S3_BUCKET_NAME = env.get('AWS_S3_BUCKET_NAME', 'filetransformeraws4')

print('Settings:')
print('connection db: {0}'.format(SQLALCHEMY_DATABASE_URI))
print('Access key aws: {0}'.format(AWS_ACCESS_KEY))
print('Secret key aws: {0}'.format(AWS_SECRET_KEY))
print('Token session aws: {0}'.format(AWS_SESSION_TOKEN))
print('Queue name aws: {0}'.format(QUEUE_NAME))
print('Bucket name aws: {0}'.format(S3_BUCKET_NAME))
