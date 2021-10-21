from flask import Blueprint
from flask_restful import Api
from api.resources import FileView, TaskResource, TaskListResource, VistaSignIn, VistaLogIn


api_bp = Blueprint('api_bp', __name__)

api = Api(api_bp)

api.add_resource(VistaSignIn, '/api/auth/signup')
api.add_resource(VistaLogIn, '/api/auth/login')
api.add_resource(TaskListResource, '/api/tasks')
api.add_resource(TaskResource, '/api/tasks/<int:id_task>')
api.add_resource(FileView, '/api/files/<int:id_task>/<string:type>')
