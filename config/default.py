PROPAGATE_EXCEPTIONS = True

# Database configuration
SQLALCHEMY_DATABASE_URI = 'sqlite:///convert.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SHOW_SQLALCHEMY_LOG_MESSAGES = False

# Bucket S3
S3_NAME = "filetransformer"
UPLOAD_DIRECTORY = "./data/input"
OUTPUT_DIRECTORY = "./data/output"
