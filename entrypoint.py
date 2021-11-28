try:
    from api import create_app

    settings_module = 'config.default'
    app = create_app(settings_module)

except ImportError as e:
    print(e.msg)
