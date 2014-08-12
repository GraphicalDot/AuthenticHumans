import os
from kombu import Exchange, Queue
BROKER_URL = 'redis://'

CELERY_QUEUES = (
		Queue('add_feed', Exchange('default', delivery_mode= 2),  routing_key='add.import'),
		Queue('multiply_feed', Exchange('default', delivery_mode=2),  routing_key='multiply.import'),
		    )

CELERY_ROUTES = {
		'tasks.add': {
				'queue': 'add_feed',
				'routing_key': 'add.import',
				},

		'tasks.multiply': {
				'queue': 'multiply_feed',
				'routing_key': 'multiply.import',
							        },
			}

#redis://:password@hostname:port/db_number #if using a remote host
#BROKER_HOST = ''
#BROKER_PORT = ''
#BROKER_USER = ''
#BROKER_PASSWORD = ''
#BROKER_POOL_LIMIT = 20

#Celery result backend settings, We are using monngoodb to store the results after running the tasks through celery
CELERY_RESULT_BACKEND = 'mongodb'

# mongodb://192.168.1.100:30000/ if the mongodb is hosted on another sevrer or for that matter running on different port or on different url on 
#the same server

CELERY_MONGODB_BACKEND_SETTINGS = {
		'host': 'localhost',
		'port': 27017,
		'database': 'celery',
#		'user': '',
#		'password': '',
		'taskmeta_collection': 'celery_taskmeta',
			}


CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT=['json']
CELERY_ENABLE_UTC = True
CELERYD_CONCURRENCY = 20
#CELERYD_LOG_FILE="%s/celery.log"%os.path.dirname(os.path.abspath(__file__))
