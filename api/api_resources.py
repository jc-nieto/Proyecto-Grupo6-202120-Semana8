from flask import Blueprint
from flask_restful import Api
from api.resources import AuthResource, FileResource, TaskResource, TaskListResource
from api.schemas.task_schema import TaskSchema

api_bp = Blueprint('api_bp', __name__)
task_schema = TaskSchema()
api = Api(api_bp)

#api.add_resource(AuthResource, '/api/auth/signup')
#api.add_resource(AuthResource, '/api/auth/login')
api.add_resource(TaskListResource, '/api/tasks')
api.add_resource(TaskResource, '/api/tasks/<int:task_id>')
#api.add_resource(FileResource, '/api/files/<filename>')
