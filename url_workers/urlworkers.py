#!/usr/bin/env python
import requests
import lxml.html
import os
import sys
import json
import time


from celery import current_app
from celery.contrib.methods import task_method

parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent)
from CloudStorage import RedisUrlWorkers

class URLWorkersLinkedin:
	def __init__(self):
		self.network_name = "linkedin"	
	
	
	@current_app.task(name="URLWorkersLinkedin.linkedin", filter=task_method, ignore_result=True)
	def linkedin(network_name="linkedin"):
		"""
		celery task name: URLWorkersLinkedin.linkedin
		celery queue: url_workers
		celery routing key: url_workers.import
		is periodic: True
		scehduled: per minute
	
		How to run celery worker: celery -A tasks worker --loglevel=info --beat

		This class will generate urls and feed into the srape_url queue of the celery stored in the celery.
		Few workers will be assigned to feed onto this queue, and will get the html which will be lying on this
		urls
		
		How it works:
			If redis database is empty
			it poulated the redis with these urls like these
			http://www.linkedin.com/directory/people-d, http://www.linkedin.com/directory/people-b, 
			http://www.linkedin.com/directory/people-c, http://www.linkedin.com/directory/people-d  ...etc
	
	
			It then calls RedisUrlWorkers class with not_scraped_by_level method, without any arguments which 
			means that this not_scraped_by_level will return all the objects stored in the redis who have 
			is_scraped False, All the urls stored in ths redis have this flag set to False, untill and unless that url is 
			a profile itself.
	
			Out of the many urls returned by not_scraped_by_level, it next it calls statis method populate_linked iterating 
			over only two urls
		"""
		
		redis_class = RedisUrlWorkers()


		#populate redis db with parent_nodes if the redis database is empty
		if redis_class.is_db_empty():
			alphabet_list = [chr(integer) for integer in range(97, 123)]
		
			for alphabet in alphabet_list:
				seed_url = "http://www.linkedin.com/directory/people-%s"%(alphabet)
				url_dict = dict()
				url_dict.update({"network_name": network_name, "name": "seed_nodes", "updated_on": int(time.time()),
					"is_profile": False, "is_scraped": False, "child_links": False, "level": int(1), 
					"parent_node": 'http://www.linkedin.com/directory/'})
				
				print url_dict
				redis_class.store_seed_url(seed_url, url_dict)
		
		
		#URLWorkersLinkedin.populate_linked("http://www.linkedin.com/directory/people-a", redis_class, network_name)
		
		
		for url in redis_class.not_scraped_by_level()[0: 2]:
			URLWorkersLinkedin.populate_linked(url, redis_class, network_name)
		return 
	

	@staticmethod
	def populate_linked(parent, redis_class, network_name):
		"""
		How it Works:
			parent argument is the seed_url for this method, This parent is certainly present in the redis
			database already, It then call for the details present for this parent present in the redis database, 
			parent_level is the level of this url in the linkedin tree.
			parent_name is the name of the parent, this has two three cases.
				case1: if the url is of the form "http://www.linkedin.com/directory/people-a" this will have seed_nodes
					its name.
				case2: if the url is of the form "http://www.linkedin.com/directory/people-a-80-14" this will have a 
					name somthing like this "Anupam Shailaj - Anupam Sharma, ma, pmp"
				case3: if the url is the url of a profile then parent_name will be the url itself

			
		case 1: this method then checks if "/dir" is present in the parent a.k.a seed_url, 
			
			if it does
			that means that this url is a dirctory of the people with common names.
			then finds: all profile links by xpath, '//*[@id="result-set"]/li/h2/strong/a'
			then store these profiles with key as their profile url and with additional dict as follows
				
			"network_name": Name of the social network i.e linkedin, 
			"name": Name of the profile name, 
			"parent_node": this is the url of the parent i.e parent a.k.a seed_url, 
			"url": url of the profile, 
			"is_profile": True, 
			"is_scraped": Because this has not been scraped yet, This flag should be changed by fetching workers
					once the html stored on this url would have been scrped by them
			
			"child_links": As this is a profile it will have no child links, last node in the tree 
			"level": parent_level+1, This is certaily at a level below the parent, so will have a level one
					more than its parent
			"updated_on": int(time.time()), epoch time when it was stored in the redis database

			it then updates parent hash in redis with all the child links
		
		case 2: If the parent a.k.a seed_url doesnt have "directory" in it, 
			if it doesnt it means that the parent a.k.a seed_url is a profile url
			And this url is already present in the redis database, so once it discovered that this is a profile
			following fields for hash will be updated in the redis
			"is_profile": True, 
			"child_links": False, 
			"updated_on": int(time.time())
	
		case 3: when this url only have more nodes attached to it

		Args:
			parent: this is the * parent url * from which the child nodes will be found
			redis_connection: RedisUrlWorkers class instance 
			network_name: in this class "linkedin"
		"""

		##TODO: Pagination have to be handled
		#This is the details of the parent node as was stored in the redis
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
			children = list()

			for element in dir_links_elems:
				url = element.attrib['href']
				url_dict = dict()
				url_dict.update({"network_name": network_name, "name": element.attrib["title"], 
					"parent_node": parent, "url": url, "is_profile": True, 
					"is_scraped": False, "child_links": False, "level": parent_level+1, "updated_on": int(time.time())})
				
				children.append(url)
				redis_class.store_seed_url(key=url, details=url_dict)

			redis_class.store_seed_url(key=parent, details={"child_links": children})
			return



		if not 'directory' in parent: #this means that this is a profile
			#In this case the parent is itself the child so its name is parent name, so dont change the parent and the level
			url_dict = dict()
			url_dict.update({"is_profile": True, "child_links": False, "updated_on": int(time.time())})
			
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
				"is_profile": False, "is_scraped": False, "updated_on": int(time.time()), "child_links": False, "parent_node": parent, "level": parent_level+1})
			
			#url_dict has now have all the details related to particular element

			seed_url_child_list.append(url)
			unscraped_child_url_list.append((url, url_dict))
		
		updated_parent_details = {"is_scraped": True, "is_profile": False, "child_links": seed_url_child_list, 
				"updated_on": int(time.time())}

		redis_class.store_seed_url(key=parent, details=updated_parent_details)

		redis_class.store_seed_url_children(unscraped_child_url_list)
		return True






