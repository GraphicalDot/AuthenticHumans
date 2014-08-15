#!/usr/bin/env python
#-*- coding: utf-8 -*-



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
	
	
	@staticmethod
	def linkedin(gcs_link):
		time.sleep(10)
		return "link parsed and saved on mongodb %s"%gcs_link
	
	
	@staticmethod
	def facebook(gcs_link):
		time.sleep(10)
		return "link parsed and saved on mongodb %s"%gcs_link
	
	
	@staticmethod
	def github(gcs_link):
		time.sleep(10)
		return "link parsed and saved on mongodb %s"%gcs_link
	
