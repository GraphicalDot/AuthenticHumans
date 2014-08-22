#-*- coding: utf-8 -*-
import redis



class RedisProxy:

	def __init__ (self, db=None):
		"""
		This class deals with the storing, creating, deleting, getting object from the proxy_list stored in the
		redis database.
		Args:
			
			For unhealthy_proxies pass redis_list_name = "unhealthy_proxies" as an argument when initiating this class

		"""
		if not db:
			self.redis_connection = redis.StrictRedis(host='localhost', port=6379, db=15)
		else:
			self.redis_connection = redis.StrictRedis(host='localhost', port=6379, db=db)

		
	def store_proxy_list(self, proxy_list, status):
		"""
		proxy_list is the list of the proxies which will be stores in the redis proxies list
		Each element is in the form of 
		{"ip": ip, "port": 1080, "type": Socks4, "country": Brazil, "latency": 30, "reliability": 90}

		status: healthy or unhealhty
		if status != "healthy":
			raise StandardError("not a valid status for proxy")
		
		if status != "unhealthy":
			raise StandardError("not a valid status for proxy")
		"""
		with self.redis_connection.pipeline() as pipe:
			try:
				for proxy in proxy_list:
					proxy["status"] = status
					pipe.hmset(proxy.get("ip"), proxy)
				pipe.execute()
			except Exception as e:
				raise StandardError(e)

	def total_proxies(self):
		proxy_list = self.redis_connection.keys()
		return proxy_list


	def proxy_details(self, proxy):
		"""
		Return keys and its values for the related proxy
		"""

		proxy_details = self.redis_connection.hgetall(proxy)
		return proxy_details


	def delete_proxy(self, proxy):
		"""
		Delete proxy
		"""
		self.redis_connection.delete(proxy)
		return 


	def healthy_proxies(self):
		"""
		returns the list of healthy proxies of the form
		[{'country': '\xc2\xa0Mexico', 'ip': '187.163.164.233', 'latency': '30', 'port': '1080', 
		'reliability': '100', 'status': 'healthy', 'type': 'Socks4'},

		{'country': '\xc2\xa0Pakistan', 'ip': '221.120.222.69', 'latency': '30', 'port': '1080', 
		'reliability': '100', 'status': 'healthy', 'type': 'Socks5'}]

		"""
		proxy_list = [self.redis_connection.hgetall(key) for key in self.redis_connection.keys() 
				if self.redis_connection.hget(key, "status") == "healthy"]


		return proxy_list
	
	def unhealthy_proxies(self):
		"""
		returns the list of unhealthy proxies
		[{'country': '\xc2\xa0Mexico', 'ip': '187.163.164.233', 'latency': '30', 'port': '1080', 
		'reliability': '100', 'status': 'unhealthy', 'type': 'Socks4'},

		{'country': '\xc2\xa0Pakistan', 'ip': '221.120.222.69', 'latency': '30', 'port': '1080', 
		'reliability': '100', 'status': 'unhealthy', 'type': 'Socks5'}]
		"""
		proxy_list = [self.redis_connection.hgetall(key) for key in self.redis_connection.keys() 
				if self.redis_connection.hget(key, "status") == "unhealthy"]
		return proxy_list



class RedisUrlWorkers:

	def __init__ (self, db=None):
		"""
		This class deals with the storing, creating, deleting, getting object from redis database which deals
		with storing social networks links
		Args:
			

		"""
		if not db:
			self.redis_connection = redis.StrictRedis(host='localhost', port=6379, db=14)
		else:
			self.redis_connection = redis.StrictRedis(host='localhost', port=6379, db=db)



	def not_scraped_by_level(self, level=None):
		"""
		This returns the number of links which are not scraped on the basis of the level, if provided in the arguments
		Args:
			level: type int
		
		"""
		##TODO : improve performance by either implementing lua script or by hscan by hscan is not been implemented by this python-redis
		if not level:
			#If the level is nor provided, this method will returns all the links present in the db which are not been scraped
			#Irrepective of the tree level they belong to
			urls = list()

			for url in self.redis_connection.keys():
				if not eval(self.redis_connection.hget(url, "is_scraped")):
					urls.append(url)
			
			return urls

		urls = list()
		for url in self.redis_connection.keys():
			#If the level is provided, this method will return all the links present in the database that were not been scraped and 
			#belongs to a particular level in the tree as specified by the level argument provided in the arguments

			is_scraped, node_level = self.redis_connection.hmget(url, "is_scraped", "level")
			if not eval(is_scraped) and int(node_level) == level:
				urls.append(url)
		return urls


	def is_db_empty(self):
		"""
		Return True if databse is empty else return False
		"""
		return not bool(self.redis_connection.keys())


	def node_details(self, node):
		"""
		Return keys and its values for the related node
		"""

		node_details = self.redis_connection.hgetall(node)
		return node_details


	def profiles_url_present(self):
		"""
		Returns the number of profiles present in the database
		"""
		##TODO: can be improved by lua script
		profiles = list()

		for url in self.redis_connection.keys():
			if eval(redis_connection.hget(url, "is_profile")):
				profiles.append(url)
		return profiles


	def store_seed_url(self, key, details):
		try:
			self.redis_connection.hmset(key, details)
		except Exception as e:
			raise StandardError(e)

	def store_seed_url_children(self, unscraped_child_url_list):
		with self.redis_connection.pipeline() as pipe:
			try:
				for child in unscraped_child_url_list:
					pipe.hmset(child[0], child[1])
				pipe.execute()
			except Exception as e:
				raise StandardError(e)


