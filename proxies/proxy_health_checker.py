#-*- coding: utf-8 -*-


import sys
import os
parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent)
from CloudStorage import RDS

class ProxyHealthCheck:

	def __init__(self):
		RDS_instance = RDS()
		self.healthy_proxies = RDS_instance.proxy_range(0, -1)
		RDS_instance = RDS(redis_list_name="unhealthy_proxies")
		self.unhealthy_proxies = RDS_instance.proxy_range(0, -1)

		print self.healthy_proxies
		print self.unhealthy_proxies


