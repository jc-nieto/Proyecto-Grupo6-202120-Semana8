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
- Crear las siguientes variables de entorno 

```	
   export FLASK_APP="entrypoint:app"
```
- Ejecución de la API
```
   export FLASK_APP="entrypoint:app"
   flask run
```
