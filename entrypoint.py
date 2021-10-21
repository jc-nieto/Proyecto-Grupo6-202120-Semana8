try:
    from api import create_app, make_celery

    settings_module = 'config.default'
    app = create_app(settings_module)
    celery_app = make_celery(app)
    
except ImportError as e:
    print(e.msg)
