try:
    from worker import create_app #, consumer

    settings_module = 'config.default'
    create_app(settings_module)
    #worker = consumer.process_messages()

    
except ImportError as e:
    print(e.msg)
