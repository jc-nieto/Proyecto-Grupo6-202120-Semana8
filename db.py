from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(session_options={"expire_on_commit": True})


class BaseModelMixin:

    query = None

    def add(self):
        db.session.add(self)
        db.session.commit()
        db.session.expire_all()

    def save(self):
        db.session.commit()
        db.session.expire_all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        db.session.expire_all()

    @classmethod
    def get_all(cls):
        db.session.expire_all()
        return cls.query.all()

    @classmethod
    def get_by_id(cls, resource_id):
        db.session.expire_all()
        return cls.query.get(resource_id)

    @classmethod
    def simple_filter(cls, **kwargs):
        db.session.expire_all()
        return cls.query.filter_by(**kwargs).all()
