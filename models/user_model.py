from db import db


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128), unique=True)
    contrasena = db.Column(db.String(50))
    tareas = db.relationship('Tarea', backref="usuario", cascade='all, delete, delete-orphan')
    __mapper_args__ = {
        'confirm_deleted_rows': False
    }
