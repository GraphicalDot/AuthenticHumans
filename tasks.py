
from celery import Celery
from celery import states
from celery.task import Task, TaskSet
from celery.result import TaskSetResult
from celery.utils import gen_unique_id, cached_property
from celery.decorators import periodic_task
from datetime import timedelta
from celery.utils.log import get_task_logger
import time
import requests
import pymongo

celery = Celery('p')

# Optional configuration, see the application user guide.
celery.config_from_object('celeryconfig')


MONGO_CONNECTION = pymongo.Connection()
DB = MONGO_CONNECTION.urls


"""
A class will generate a list of url to scrape. Depending upon the method called scrape_url queue will be populated with the urls
These urls will then be feeded to some celery workers to get the html from these urls.

Upon success, These html dom will be stored on Google cloud storage, On success Google cloud storage will generate a url, 
These urls's will then be populated into another queue gcs_links.
This url_html queue will then be feeded to another set of workers to parse the html with lxml and then store the results into mongodb

Two queues
	1. scrape_url : which will have the urls to be scraped.
	2. gcs_links: which will have the google cloud storage links.

Workers
	1.Which will feed on scrape_url queue to get the html lying on url
	2.Which will feed on gcs_links queue to parse the html and store in mongodb


"""

class GenerateURLs:
	"""
	This function will generate urls and feed into the srape_url queue of the celery stored in the celery.
	Few workers will be assigned to feed onto this queue, and will get the html which will be lying on this 
	urls

	Args:
		name: name of the site
		counter: upto which alphabet the urls were scraped or for that matter some other counter depending 
		upon the website
	"""

	def __init__(self):
		pass
	
	@staticmethod
	def linkedin(counter):
		seed_url = ""
		urls = list()
		new_counter = None
		return (new_counter, range(0, 100))

	@staticmethod
	def facebook(counter):
		seed_url = ""
		urls = list()
		new_counter = None
		return (new_counter, range(0, 100))

	@staticmethod
	def github(counter):
		seed_url = ""
		urls = list()
		new_counter = None
		return (new_counter, range(0, 100))



@celery.task(ignore_result=True)
def fetch_html(url):
	"""
	This is the function which gets the html lying on the url and then save it to google cloud staorage

	"""
	time.sleep(10)
	#result = requests.get(url)
	return 


@celery.task
def error_handler(uuid):
	result = AsyncResult(uuid)
	exc = result.get(propagate=False)
	print('Task {0} raised exception: {1!r}\n{2!r}'.format(uuid, exc, result.traceback))


class CallBackTask(Task):
	abstract = True
	accept_magic_kwargs = False
	
	def after_return(self, args, kwargs):
		"""
		if self.request.taskset:
			callback = self.request.kwargs.get("callback")
			
			if callback:
                		setid = self.request.taskset
				# task set must be saved in advance, so the task doesn't
				# try to restore it before that happens.  This is why we
				# use the `apply_presaved_taskset` below.
				result = TaskSetResult.restore(setid)
				current = self.redis.incr("taskset-" + setid)
				if current >= result.total:
					r = subtask(callback).delay(result.join())
		"""
		print "completed"

	def on_success(self, retval, task_id, args, kwargs):
		print task_id
		print retval
		print "task has been completed"
		pass

	def on_failure(self, exc, task_id, args, kwargs, einfo):
		print task_id
		print retval
		print "task failed"
		pass

	@cached_property
	def redis(self):
		pass


#@celery.task(base=CallBackTask)
@celery.task(ignore_result=True)
def populate_scrape_url(name):
	"""
	This function will call GenerateURLs class
	This will be used to get urls and then populate the srape_url queue
	Args:
		name: name of the site for which the urls to be populated

	"""
	collection = eval("DB.%s"%name)
	#counter = list(collection.find())[0].get("counter")	
	counter = None	

	if name == "LINKEDIN":
		instance = GenerateURLs.linkedin(counter)
		new_counter = instance[0]
		urls = instance[1]
		for url in urls:
			fetch_html.apply_async([url], retry=True, retry_policy={'max_retries': 3, 
				'interval_start': 0, 'interval_step': 0.2, 'interval_max': 0.2, }, link_error=error_handler.s())

		#TODO: update counter by inserting the new counter in mongodb

	if name == "FACEBOOK":
		instance = GenerateURLs.facebook(counter)
		for url in urls:
			fetch_html.apply_async([url], retry=True, retry_policy={'max_retries': 3, 
				'interval_start': 0, 'interval_step': 0.2, 'interval_max': 0.2, })
		#TODO: update counter by inserting the new counter in mongodb
		
	if name == "GITHUB":
		instance = GenerateURLs.github(counter)
		new_counter = instance[0]
		urls = instance[1]
		for url in urls:
			fetch_html.apply_async([url], retry=True, retry_policy={'max_retries': 3, 
				'interval_start': 0, 'interval_step': 0.2, 'interval_max': 0.2, })
		#TODO: update counter by inserting the new counter in mongodb
			
	pass




