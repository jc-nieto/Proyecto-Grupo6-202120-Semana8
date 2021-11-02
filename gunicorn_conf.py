worker_class = 'sync'
loglevel = 'debug'
accesslog = '/home/ubuntu/gunicorn/access_log_yourapp'
acceslogformat = "%(h)s %(l)s %(u)s %(t)s %(r)s %(s)s %(b)s %(f)s %(a)s"
errorlog = '/home/ubuntu/gunicorn/error_log_yourapp'
