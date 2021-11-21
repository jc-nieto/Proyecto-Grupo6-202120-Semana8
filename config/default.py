PROPAGATE_EXCEPTIONS = True

# Database configuration
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:gerzonEsUnCrack@mydb.cg99sgyfzyzj.us-east-1.rds.amazonaws.com:3306/myDB'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SHOW_SQLALCHEMY_LOG_MESSAGES = False
JWT_SECRET_KEY = 'frase-secreta'
CELERY_BROKER_URL='redis://172.16.1.101:6379/0',
CELERY_RESULT_BACKEND='redis://localhost:6379/0'
