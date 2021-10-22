from flask import Flask, jsonify
from flask_restful import Api

from api.resources import jwt
from api.tasks import celery_app
from sqlalchemy.exc import IntegrityError
from common.error_handling import ObjectNotFound, AppErrorBaseClass, NotAllowed, NotReady
from db import db
from api.api_resources import api_bp
from ext import marshmallow, migrate


def create_app(settings_module):
    app = Flask(__name__)
    app.config.from_object(settings_module)
    app.app_context().push()

    # Init extensions
    db.init_app(app)
    db.create_all()
    marshmallow.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Catch all errors 404
    Api(app, catch_all_404s=True)

    # Disable strict URL finishing mode with /
    app.url_map.strict_slashes = False

    # Register the blueprints
    app.register_blueprint(api_bp)

    # Register custom error handlers
    register_error_handlers(app)
    return app

def make_celery(app):

    celery_app.conf.update(app.config)

    class ContextTask(celery_app.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app.Task = ContextTask
    return celery_app

def register_error_handlers(app):

    @app.errorhandler(Exception)
    def handle_exception_error(e):
        return jsonify({'msg': 'Internal server error', 'error': str(e)}), 400

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(e):
        db.session.rollback()
        return jsonify({'msg': 'El usuario ya existe', 'error': str(e)}), 400


    @app.errorhandler(405)
    def handle_405_error(e):
        return jsonify({'msg': 'Method not allowed'}), 405

    @app.errorhandler(403)
    def handle_403_error(e):
        return jsonify({'msg': 'Forbidden error'}), 403

    @app.errorhandler(404)
    def handle_404_error(e):
        return jsonify({'msg': 'Not Found error'}), 404

    @app.errorhandler(AppErrorBaseClass)
    def handle_app_base_error(e):
        return jsonify({'msg': str(e)}), 400

    @app.errorhandler(ObjectNotFound)
    def handle_object_not_found_error(e):
        return jsonify({'msg': str(e)}), 404

    @app.errorhandler(NotAllowed)
    def handle_not_allowed(e):
        return jsonify({'msg': str(e)}), 401

    @app.errorhandler(NotReady)
    def handle_not_ready(e):
        return jsonify({'msg': str(e)}), 400
