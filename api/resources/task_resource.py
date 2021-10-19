from flask import request
from flask_restful import Resource

from common.error_handling import ObjectNotFound
from models import Task
from ..schemas import TaskSchema

task_schema = TaskSchema()


class TaskResource(Resource):

    def get(self, task_id):
        task = Task.get_by_id(task_id)
        if task is None:
            raise ObjectNotFound('The task does not exist')
        return task_schema.dump(task)

    def post(self):
        return 'TO DO'

    def put(self, task_id):
        return 'TO DO'

    def delete(self, task_id):
        return 'TO DO'


class TaskListResource(Resource):

    def get(self):
        maximum = request.args.get('max')
        order = request.args.get('order')
        return 'TO DO'
