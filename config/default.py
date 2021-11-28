PROPAGATE_EXCEPTIONS = True
APP_DEV = False

# Database configuration
# SQLALCHEMY_DATABASE_URI = 'sqlite:///convert.db'
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:gerzonEsUnCrack@mysql-database-01.ccieufxfelfu.us-east-1.rds.amazonaws.com:3306/convertion_db'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:gerzonEsUnCrack@mydb.cg99sgyfzyzj.us-east-1.rds.amazonaws.com:3306/myDB'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SHOW_SQLALCHEMY_LOG_MESSAGES = False
JWT_SECRET_KEY = 'frase-secreta'
CELERY_BROKER_URL = 'redis://172.16.1.102:6379/0',
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# AWS Credentials
AWS_ACCESS_KEY = "ASIAXPWA7CPL7LCAA4VP"
AWS_SECRET_KEY = "r4oLPayAfNHiJIybkryPaNnbmPLlk2wU+2lwBmas"
AWS_SESSION_TOKEN = "FwoGZXIvYXdzEP///////////wEaDJpablgf/huB7Q7zdSLLAWILG4HY3f7tMXESrmqkio2iU0jc1TxvbusNxaSp1IxJus1RcV828/MKtHGNPrjMNUQ9dF9ZOq35I164XJC6rf/XVipTJN343sYv46araKPqMElkhi3HlNpgHP5AXZTFP3a3jlXrnZn8vKE09wJsWXBcyMct6dLiiFRm768uEqMiLYr9rIn+yWU6t+Q8L4XxS2KCSRir1+U/6J+BWAiK91rJzg8isELsanrFaLIpOPGgCxfMEcI0BCtCWucLZ7fcIvOsRaLhhascyEjAKNuwjI0GMi2mu4zZjgRKWlD9M1/hN9L+Y7eRj+XbplAoWRwUVcmPwFaSfjpEROccmXClHQ8="

# SQS
QUEUE_NAME = "consumers-queue.fifo"

# Bucket S3
S3_BUCKET_NAME = "filetransformer"
# S3_BUCKET_NAME = "bucket-files-convertion"
