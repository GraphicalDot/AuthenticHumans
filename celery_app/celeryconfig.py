import os
from kombu import Exchange, Queue
from celery.schedules import crontab
#from kombu import serialization
#serialization.registry._decoders.pop("application/x-python-serialize")
#BROKER_URL = 'redis://'
BROKER_URL = 'redis://localhost:6379/0'

CELERY_QUEUES = (
		Queue('scrape_url', Exchange('default', delivery_mode= 2),  routing_key='scrape_url.import'),
		Queue('gcs_links', Exchange('default', delivery_mode=2),  routing_key='gcs_links.import'),
		Queue('parse_html', Exchange('default', delivery_mode=2),  routing_key='parse_html.import'),
		    )

CELERY_ROUTES = {
		'tasks.populate_scrape_url': {
				'queue': 'scrape_url',
				'routing_key': 'scrape_url.import',
				},

		'tasks.fetch_html': {
				'queue': 'gcs_links',
				'routing_key': 'gcs_links.import',
							        },
		
		'ParsingWorkersTask.linkedin': {
				'queue': 'parse_html',
				'routing_key': 'parse_html.import',
							        },
		
		'ParsingWorkersTask.facebook': {
				'queue': 'parse_html',
				'routing_key': 'parse_html.import',},

		'ParsingWorkersTask.github': {
				'queue': 'parse_html',
				'routing_key': 'parse_html.import',
							        },
			}


"""
CELERYBEAT_SCHEDULE = {
	'every-minute': {
		'task': 'tasks.populate_scrape_url',
			'schedule': crontab(minute='*/1'),
			'args': ("LINKEDIN"),
			},
	}


"""

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


#CELERY_TASK_SERIALIZER = 'json'
#CELERY_RESULT_SERIALIZER = 'json'
#CELERY_ACCEPT_CONTENT=['application/json']
CELERY_ENABLE_UTC = True
CELERYD_CONCURRENCY = 20
#CELERYD_LOG_FILE="%s/celery.log"%os.path.dirname(os.path.abspath(__file__))
CELERY_DISABLE_RATE_LIMITS = True
CELERY_RESULT_PERSISTENT = True #Keeps the result even after broker restart


