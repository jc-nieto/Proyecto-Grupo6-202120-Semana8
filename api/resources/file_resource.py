from flask_restful import Resource
from flask_jwt_extended import jwt_required,get_jwt_identity
from flask import send_file

from models import Tarea
from common.error_handling import NotAllowed, NotReady, ObjectNotFound,NotAllowed


class FileView(Resource):
    @jwt_required()
    def get(self,id_task,type):
        tarea:Tarea = Tarea.get_by_id(id_task)
        if tarea.usuario_task != get_jwt_identity():
            raise NotAllowed('No tiene permisos para realizar ésta acción')
        if tarea is None:
            raise ObjectNotFound
        if type =='input':
            path = tarea.inputpath.replace('./data','../data')
            return send_file(path)
        elif tarea.estado == 'processed' and type =='output':
            path = tarea.outputpath.replace('./data','../data')
            return send_file(path)
        else:
            raise NotReady('El archivo aún no esta listo')
