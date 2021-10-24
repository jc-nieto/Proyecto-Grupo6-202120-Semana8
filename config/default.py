PROPAGATE_EXCEPTIONS = True

# Database configuration
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:12345@localhost:5432/convertdb'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SHOW_SQLALCHEMY_LOG_MESSAGES = False
JWT_SECRET_KEY = 'frase-secreta'
CELERY_BROKER_URL='redis://localhost:6379/0',
CELERY_RESULT_BACKEND='redis://localhost:6379/0'
