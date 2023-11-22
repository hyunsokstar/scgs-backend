# gunicorn config for ch8 project
wsgi_app = 'config.wsgi'

bind = 'unix:/tmp/gun.sock'
daemon = True
accesslog = '/home/ubuntu/scgs_back/logs/access.log'
errorlog = '/home/ubuntu/scgs_back/logs/error.log'


