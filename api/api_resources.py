from flask import Blueprint
from flask_restful import Api
from api.resources import FileResource, TaskResource, TaskListResource, SignInResource, LogInResource


api_bp = Blueprint('api_bp', __name__)

api = Api(api_bp)

api.add_resource(SignInResource, '/api/auth/signup')
api.add_resource(LogInResource, '/api/auth/login')
api.add_resource(TaskListResource, '/api/tasks')
api.add_resource(TaskResource, '/api/tasks/<int:id_task>')
api.add_resource(FileResource, '/api/files/<int:id_task>/<string:type>')
