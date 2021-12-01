# Cloud conversion tool

## How to run

### Api Back
- Instalación de libreria ffmpeg
```	
   sudo apt	update
   sudo apt install ffmpeg
```
- Instalación de las dependencias
```	
   python3 -m pip install -r requirements.txt 	
```
- Creación de las variables de entorno
```	
   export FLASK_APP="entrypoint:app"
   export DB_USER="set_your_db_user"
   export DB_PASSWORD="set_your_db_user"
   export DB_HOST="set_your_db_host"
   export DB_PORT="set_your_db_port"
   export DB_NAME="set_your_db_name"
   export AWS_ACCESS_KEY="set_your_aws_access_key"
   export AWS_SECRET_KEY="set_your_aws_secret_key"
   export AWS_SESSION_TOKEN="set_your_aws_session_token"
   export AWS_QUEUE_NAME="set_your_aws_queue_name"
   export AWS_S3_BUCKET_NAME="set_your_aws_queue_name"
```
- Ejecución de la API
```
   flask run
```
