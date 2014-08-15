#!/usr/bin/env python

class URLWorkersTask:
	"""
	This class will generate urls and feed into the srape_url queue of the celery stored in the celery.
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




