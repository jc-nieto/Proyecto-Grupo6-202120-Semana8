PROPAGATE_EXCEPTIONS = True
APP_DEV = False

# Database configuration
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:gerzonEsUnCrack@mydb.cg99sgyfzyzj.us-east-1.rds.amazonaws.com:3306/myDB'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SHOW_SQLALCHEMY_LOG_MESSAGES = False

# AWS Credentials
AWS_ACCESS_KEY = "ASIAXPWA7CPLZSVBBTTX"
AWS_SECRET_KEY = "1TEZVXB4wFmH7J3FCjvnU1O9wwl0vK+TEUF12izc"
AWS_SESSION_TOKEN = "FwoGZXIvYXdzEAYaDD6MlsVx+pliA3+fiyLLAWzsbgKkIcPKCtswICH5G2wrTFubut3ajMpAcvy4XwbbBAO6gfibeJPxZvZRYMCRKBsTC1h52/Q+vCLkruwEw+TJZmkalAezd55TZxFjBKEcRXZNhqqJJlpesXNVfD9sRwGDL/4vupGC3a4E/E74F1tDQJGJLDUG0pN2Npp/tpKGZUbRFOuhBZ223HPQsgygc+rJm63j9zx4bL1ZmZ2Y6qDbU1s5IGx5ryt+rIzSTm0c5s/dZXNH2BTrc86LGWSgsKZZzMlOY/CadX3tKO/3jY0GMi2c2S2HDbjjntuzotc4kOaQ3CIv12rsdfF3+gh3Z9GAwKJzSY6C0m4dhB8XGXQ="

# SQS
QUEUE_NAME = "consumers-queue.fifo"

# Bucket S3
S3_BUCKET_NAME = "filetransformer"
#S3_BUCKET_NAME = "bucket-files-convertion"
