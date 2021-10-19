from db import db, BaseModelMixin


class Task(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    # Check
    inputpath = db.Column(db.String(128))
    outputpath = db.Column(db.String(128), nullable=True)
    estado = db.Column(db.String(128), default='uploaded', nullable=True)


