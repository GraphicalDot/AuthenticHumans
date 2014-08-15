#!/usr/bin/env python
#-*- coding: utf-8 -*-
import time
import os
import sys
parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent)
from celery_app.App import app
from celery.contrib.methods import task_method
from celery import current_app

class ParsingWorkersTask:
	"""
	This is the class used to parse the html stored on the gcs link based on the name of the website
	from which the fetching workers had scraped this html.

	This class also is responsible to store the html on the disk which will then be sved to gcs by cronjob
	mthod Arg:
		gcs_link: link of the gcs on which the html had been saved.

	Return:
		True of false
		Based on the succes and failure
	"""


	def __init__(self):
		pass
	
	#@current_app.task(filter=task_method) if only one celery app exists
	@current_app.task(name="ParsingWorkersTask.linkedin", filter=task_method)
	def linkedin(gcs_link):
		time.sleep(10)
		return {"result": True, "messege": "LINKEDIN link parsed and saved on mongodb %s"%gcs_link}
	
	
	@current_app.task(name="ParsingWorkersTask.facebook", filter=task_method)
	def facebook(gcs_link):
		time.sleep(10)
		return {"result": True, "messege": "FACEBOOK link parsed and saved on mongodb %s"%gcs_link}
	
	
	@current_app.task(name="ParsingWorkersTask.github", filter=task_method)
	def github(gcs_link):
		time.sleep(10)
		return {"result": True, "messege": "GITHUB link parsed and saved on mongodb %s"%gcs_link}
	
