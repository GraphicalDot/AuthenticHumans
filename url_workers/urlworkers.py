#!/usr/bin/env python
import requests
import lxml.html
import os
import sys
import json

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
				url_dict.update({"network_name": network_name, "name": "seed_nodes", 
					"is_profile": False, "is_scraped": False, "child_links": False, "level": int(1), 
					"parent_node": 'http://www.linkedin.com/directory/'})
				
				print url_dict
				redis_class.store_seed_url(seed_url, url_dict)
		
		
		#URLWorkersLinkedin.populate_linked("http://www.linkedin.com/directory/people-a", redis_class, network_name)
		
		
		for url in redis_class.not_scraped_by_level(4)[0:10]:
			print url
			URLWorkersLinkedin.populate_linked(url, redis_class, network_name)
		
		
		return 
	

	@staticmethod
	def populate_linked(parent, redis_class, network_name):
		"""
		Args:
			parent: this is the * parent url * from which the child nodes will be found
			redis_connection: RedisUrlWorkers class instance 
			network_name: in this class "linkedin"
			seed_name: name of the seed, in the case of staring nodes, it will be None but there after it will certainly
				have name attached to it.

		
		##TODO: Pagination have to be handled
		"""
		#this is the details of the parent node as was stored in the redis
		parent_details = redis_class.node_details(parent)
		parent_level = int(parent_details.get("level"))
		
		parent_name = parent_details.get("name")



		parent_node_html = requests.get(parent)
		parent_node_tree = lxml.html.fromstring(parent_node_html.content)
		
		# members with a same name are shown in a different view
		# eg. http://www.linkedin.com/pub/dir/Abood/Salah
		
		
		##This if statement will be executed only if we come across a directory of profile pages
		if '/dir/' in parent:
			dir_links_elems = parent_node_tree.xpath('//*[@id="result-set"]/li/h2/strong/a')

			for element in dir_links_elems:
				url = element.attrib['href']
				url_dict = dict()
				url_dict.update({"network_name": network_name, "name": element.attrib["title"], 
					"parent_node": parent, "url": element.attrib["href"], "is_profile": True, 
					"is_scraped": False, "child_links": False, "level": parent_level+1})
				
				redis_class.store_seed_url(key=url, details=url_dict)
			return



		if not 'directory' in parent: #this means that this is a profile
			#In this case the parent is itself the child so its name is parent name, so dont change the parent and the level
			url_dict = dict()
			url_dict.update({"network_name": network_name, "name": parent_name, "url": parent,
					"is_profile": True, "is_scraped": False, "child_links": False,})
			
			redis_class.store_seed_url(key=parent, details=url_dict)
			#is_scraped parameter will be changed by parsing workers
			return


		unscraped_child_url_list = list() #this will have the child nodes of the seed url with all the details
		seed_url_child_list = list() #This will have the child nodes of the seed url with only the urls


		dir_links_elems = parent_node_tree.xpath('//*[@id="body"]/div/ul[2]/li/a') #will have all the hyperlinks
		
		
		for element in dir_links_elems:
			url_dict = dict()
			
			url = 'http://www.linkedin.com{link_path}'.format(link_path=element.attrib['href'])
			
			url_dict.update({"network_name": network_name, "name": element.text.strip(), 
				"is_profile": False, "is_scraped": False, "child_links": False, "parent_node": parent, "level": parent_level+1})
			
			#url_dict has now have all the details related to particular element

			seed_url_child_list.append(url)
			unscraped_child_url_list.append((url, url_dict))
		
		updated_parent_details = {"is_scraped": True, "is_profile": False, "child_links": seed_url_child_list}

		redis_class.store_seed_url(key=parent, details=updated_parent_details)

		redis_class.store_seed_url_children(unscraped_child_url_list)
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



if __name__ == "__main__":
	URLWorkersLinkedin.linkedin()
