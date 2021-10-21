from db import BaseModelMixin, db


class Tarea(db.Model,BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128))
    inputpath = db.Column(db.String(128))
    outputpath = db.Column(db.String(128), nullable=True)
    estado = db.Column(db.String(128), default='uploaded', nullable=True)
    usuario_task = db.Column(db.Integer, db.ForeignKey("usuario.id"))
