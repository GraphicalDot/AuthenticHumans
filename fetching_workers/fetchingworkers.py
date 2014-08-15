#!/usr/bin/env python
#-*- coding: utf-8 -*-

import time
import random


class FetchingWorkersTask:
	"""
	Task of this class is to get the html lying on the url given to it
	and stores it into the google cloud storage
	"""
	def __init__(self):
		pass

	@staticmethod
	def html(url):
		time.sleep(10)
		return "http://s3.xyz.com/%s"%random.randint(20, 300)



