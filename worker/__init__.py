from flask import Flask
from db import db
import logging
import consumer

def create_app(settings_module):
    app = Flask(__name__)
    app.config.from_object(settings_module)
    app.app_context().push()
    gunicorn_error_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers.extend(gunicorn_error_logger.handlers)
    app.logger.setLevel(logging.DEBUG)
    app.logger.debug('this will show in the log')

    # Init extensions
    db.init_app(app)
    db.create_all()

    # Disable strict URL finishing mode with /
    app.url_map.strict_slashes = False
    worker = consumer.process_messages()
    return app
