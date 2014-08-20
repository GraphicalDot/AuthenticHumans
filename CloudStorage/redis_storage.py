#-*- coding: utf-8 -*-
import redis



class RDS:

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






