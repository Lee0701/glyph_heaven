
from datetime import datetime
import os

now = datetime.now().strftime('%Y-%m-%d_%H')

if not os.path.exists('logs'):
    os.makedirs('logs', exist_ok=True)

bind = '0.0.0.0:80'
workers = 2
reload = True
accesslog = f'logs/access_{now}.log'
errorlog = f'logs/error_{now}.log'
loglevel = 'info'
