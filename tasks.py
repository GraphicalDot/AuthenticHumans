from __future__ import absolute_import

from celery import Celery
from celery import states
from celery.task import Task, TaskSet
from celery.result import TaskSetResult
from celery.utils import gen_unique_id, cached_property
import time
import requests


celery = Celery('p')

# Optional configuration, see the application user guide.
celery.config_from_object('celeryconfig')

@celery.task
def get_html(url):
	time.sleep(1)
	result = requests.get(url)
	return result.content



class CallBackTask(Task):
	abstract = True
	accept_magic_kwargs = False
	
	def after_return(self, args, kwargs):
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


@celery.task(base=CallBackTask)
def add(a, b):
	return a+b


@celery.task(base=CallBackTask)
def multiply(a, b):
	return a*b



