#-*- coding: utf-8 -*-

import time
import random
import requests
import sys
import os
from celery import current_app

parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent)
from celery_app.App import app
from CloudStorage import GCS

class FetchingWorkersTask:
	"""
	Task of this class is to get the html lying on the url given to it
	and stores it into the google cloud storage
	"""
	def __init__(self):
		pass

	@classmethod
	def html(cls, url):
		time.sleep(10)
		result = cls.scrape(url)
		if result:
			return result




	@classmethod
	def scrape(cls, url):
		r = requests.get(url)
		if r.status_code == 200:
			return r.text
		return False


