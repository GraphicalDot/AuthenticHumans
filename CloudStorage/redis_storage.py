#-*- coding: utf-8 -*-
import redis



class RDS:

	def __init__ (self, redis_list_name=None, db=None):
		"""
		This class deals with the storing, creating, deleting, getting object from the proxy_list stored in the
		redis database.
		Args:
			

		"""
		if not db:
			self.redis_connection = redis.StrictRedis(host='localhost', port=6379, db=15)
		else:
			self.redis_connection = redis.StrictRedis(host='localhost', port=6379, db=db)

		if not redis_list_name:
			self.redis_list_name = "proxies"
		else:
			self.redis_list_name = redis_list_name

		
	def store_proxy_list(self, proxy_list):
		"""
		proxy_list is the list of the proxies which will be stores in the redis proxies list
		Each element is in the form of 
		{"ip": ip, "port": 1080, "type": Socks4, "country": Brazil, "latency": 30, "reliability": 90}

		"""
		
		with self.redis_connection.pipeline() as pipe:
			try:
				for proxy in proxy_list:
					pipe.rpush(self.redis_list_name, proxy)
			
				pipe.execute()
			except Exception as e:
				raise StandardError(e)

	def total_proxies(self):
		number = self.redis_connection.lrange(self.redis_list_name, 0, -1)
		return number


	def proxy_range(self, start, stop):
		proxies = self.redis_connection.lrange(self.redis_list_name, start, stop)
		return proxies


	def proxy_on_index(self, index):
		"""
		Returns proxy on the basis of the index given in the args
		"""
		proxy = self.redis_connection.lindex(self.redis_list_name, index)
		return proxy

	def del_lkey(self, index):
		"""
		This method deletes the left key and return the proxy present on the position 0
		"""
		proxy = self.redis_connection.lindex("proxies", 0)
		self.redis_connection.lpop("proxies")
		return proxy

	def del_rkey(self, index):
		"""
		This method deletes the right key and return the proxy present on the position 0
		"""
		proxy = self.redis_connection.lindex("proxies", -1)
		self.redis_connection.lpop("proxies")
		return proxy







