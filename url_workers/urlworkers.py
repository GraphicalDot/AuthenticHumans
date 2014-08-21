#!/usr/bin/env python
import requests
import lxml.html
import os
import sys


parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent)
from CloudStorage import RedisUrlWorkers

class URLWorkersLinkedin:
	"""
	This class will generate urls and feed into the srape_url queue of the celery stored in the celery.
	Few workers will be assigned to feed onto this queue, and will get the html which will be lying on this
	urls
		
	"""
	def __init__(self):
		self.network_name = "linkedin"	
	
	
	@staticmethod
	def linkedin(network_name="linkedin"):
		"""Recursively collect the profile URLs of members from the LinkedIn directory.
		Args:
			seed_url -- the directory URL to start fetching from.
		"""
		
		redis_class = RedisUrlWorkers()



		#populate redis db with parent_nodes if the redis database is empty
		if redis_class.is_db_empty():
			alphabet_list = [chr(integer) for integer in range(97, 123)]
		
			for alphabet in alphabet_list:
				seed_url = "http://www.linkedin.com/directory/people-%s"%(alphabet)
				url_dict = dict()
				url_dict.update({"network_name": network_name, "name": "parent_nodes", 
					"is_profile": False, "is_scraped": False, "child_links": False, "level": 1, "parent_node": None})
				
				redis_class.store_seed_url(key=url, details=url_dict)
		


		return 
	

	@staticmethod
	def populate_linked(seed_url, network_name, seed_name=None):
		
		p = requests.get(seed_url)
		page = lxml.html.fromstring(p.content)
		
		# members with a same name are shown in a different view
		# eg. http://www.linkedin.com/pub/dir/Abood/Salah
		
		
		##This if statement will be executed only if we come across a directory of profile pages
		if '/dir/' in seed_url:
			dir_links_elems = page.xpath('//*[@id="result-set"]/li/h2/strong/a')

			for element in dir_links_elems:
				url = element.attrib['href']
				url_dict = dict()
				url_dict.update({"network_name": network_name, "name": element.attrib["title"], 
					"is_profile": True, "is_scraped": False, "child_links": False,})
				
				RedisUrlWorkers.store_seed_url(key=url, details=url_dict)
			return



		if not 'directory' in seed_url or '/dir/' in seed_url: #this means that this is a profile
			url_dict = dict()
			url_dict.update({"network_name": network_name, "name": seed_name, 
					"is_profile": True, "is_scraped": False, "child_links": False,})
			
			RedisUrlWorkers.store_seed_url(key=seed_url, details=url_dict)
			#is_scraped parameter will be changed by parsing workers
			return


		unscraped_child_url_list = list() #this will have the child nodes of the seed url with all the details
		seed_url_child_list = len() #This will have the child nodes of the seed url with only the urls


		dir_links_elems = page.xpath('//*[@id="body"]/div/ul[2]/li/a')
		
		
		for element in dir_links_elems:
			url_dict = dict()
			
			url = 'http://in.linkedin.com{link_path}'.format(link_path=element.attrib['href'])
			
			url_dict.update({"network_name": network_name, "name": element.text.strip(), 
				"is_profile": False, "is_scraped": False, "child_links": False,})
			
			#url_dict has now have all the details related to particular element

			seed_url_child_list.append(url)
			unscraped_child_url_list.append((url, url_dict))
		
		seed_url_details = {"network_name": network_name, "name": name, "is_scraped": True, "is_profile": False, 
					"child_links": seed_url_child_list}

		RedisUrlWorkers.store_seed_url(key=seed_url, details=seed_url_details)
		RedisUrlWorkers.store_seed_url_children(unscraped_child_url_list)
		return True



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




