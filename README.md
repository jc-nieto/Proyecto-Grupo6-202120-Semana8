# Cloud conversion tool

## How to run

### Worker
- Instalación de libreria ffmpeg
```	
   sudo apt update
   sudo apt install ffmpeg
```
- Instalación de las dependencias
```	
   python3 -m pip install -r requirements.txt 	
```
- Ejecución del worker
```
   export FLASK_APP="entrypoint:worker"
   flask run
```
