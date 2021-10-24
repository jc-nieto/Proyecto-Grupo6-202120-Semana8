# Cloud conversion tool

## How to run

### Api Back
- Instalación de las dependencias
```	
   python3 -m pip install -r requirements.txt 	
```
- Crear las siguientes variables de entorno 

```	
   export FLASK_APP="entrypoint:app"
```
- Ejecución de la API desde la raiz del proyecto
```	
   flask run
```
- Ejecución de plataforma de mensajeria desde la raiz del proyecto
```
   celery -A entrypoint.celery_app worker -l info -Q procesar
```
