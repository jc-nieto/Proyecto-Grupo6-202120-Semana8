from db import BaseModelMixin, db
from sqlalchemy.sql import func


class Tarea(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128))
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    inputpath = db.Column(db.String(128))
    outputpath = db.Column(db.String(128), nullable=True)
    estado = db.Column(db.String(128), default='uploaded', nullable=True)
    usuario_task = db.Column(db.Integer, db.ForeignKey("usuario.id"))
