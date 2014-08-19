#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

class Proxies:
	"""
	This is the class used to extract and populate proxies from different website
	Proxies 
	Args:
		number_of_proxies:
			type int, number of proxies to be populated
		type_of_proxy:
			type str, type of proxy to be populated socks4 or socks5
		country:
			type str, proxies if required from a particular country india, us, uk etc
			(u'Any country', u''), (u'Afghanistan', u'AF'), (u'Albania', u'AL'), (u'Argentina', u'AR'), 
			(u'Armenia', u'AM'), (u'Bangladesh', u'BD'), (u'Belarus', u'BY'), (u'Belgium', u'BE'), (u'Benin', u'BJ'), 
			(u'Bolivia', u'BO'), (u'Bosnia and Herzegovina', u'BA'), (u'Brazil', u'BR'), (u'Bulgaria', u'BG'), 
			(u'Cambodia', u'KH'), (u'Cameroon', u'CM'), (u'Canada', u'CA'), (u'Chad', u'TD'), (u'Chile', u'CL'), 
			(u'China', u'CN'), (u'Colombia', u'CO'), (u"Cote D'Ivoire (Ivory Coast)", u'CD'), (u'Croatia (Hrvatska)', u'HR'), 
			(u'Cuba', u'CU'), (u'Cyprus', u'CY'), (u'Czech Republic', u'CZ'), (u'Denmark', u'DK'), (u'Ecuador', u'EC'), 
			(u'Egypt', u'EG'), (u'El Salvador', u'SV'), (u'Ethiopia', u'ET'), (u'European Union', u'EU'), (u'France', u'FR'), 
			(u'Georgia', u'GE'), (u'Germany', u'DE'), (u'Ghana', u'GH'), (u'Great Britain (UK)', u'GB'), (u'Greece', u'GR'), 
			(u'Honduras', u'HN'), (u'Hong Kong', u'HK'), (u'Hungary', u'HU'), (u'India', u'IN'), (u'Indonesia', u'ID'), 
			(u'Iran', u'IR'), (u'Iraq', u'IQ'), (u'Israel', u'IL'), (u'Italy', u'IT'), (u'Japan', u'JP'), (u'Kazakhstan', u'KZ'), 
			(u'Kenya', u'KE'), (u'Korea (South)', u'KR'), (u'Kuwait', u'KW'), (u'Lebanon', u'LB'), (u'Liberia', u'LR'), 
			(u'Lithuania', u'LT'), (u'Luxembourg', u'LU'), (u'Madagascar', u'MG'), (u'Malaysia', u'MY'), (u'Mali', u'ML'), 
			(u'Mauritius', u'MU'), (u'Mexico', u'MX'), (u'Mongolia', u'MN'), (u'Mozambique', u'MZ'), (u'Myanmar', u'MM'), 
			(u'Nepal', u'NP'), (u'Netherlands', u'NL'), (u'Nigeria', u'NG'), (u'Pakistan', u'PK'), (u'Palestine', u'PS'), 
			(u'Panama', u'PA'), (u'Paraguay', u'PY'), (u'Peru', u'PE'), (u'Philippines', u'PH'), (u'Poland', u'PL'), 
			(u'Puerto Rico', u'PR'), (u'Romania', u'RO'), (u'Russian Federation', u'RU'), (u'Saudi Arabia', u'SA'), 
			(u'Singapore', u'SG'), (u'Slovak Republic', u'SK'), (u'Slovenia', u'SI'), (u'South Africa', u'ZA'), (u'Spain', u'ES'), 
			(u'Sri Lanka', u'LK'), (u'Sudan', u'SD'), (u'Sweden', u'SE'), (u'Switzerland', u'CH'), (u'Taiwan', u'TW'), 
			(u'Tanzania', u'TZ'), (u'Thailand', u'TH'), (u'Tunisia', u'TN'), (u'Turkey', u'TR'), (u'Ukraine', u'UA'), 
			(u'United Arab Emirates', u'AE'), (u'United States', u'US'), (u'Vanuatu', u'VU'), (u'Venezuela', u'VE'), 
			(u'Viet Nam', u'VN'), (u'Zambia', u'ZM'), (u'Zimbabwe', u'ZW')

		latency:
			type int, latency required in a proxy, values can be 1000, 3000, 5000, or 10000, 
			which corresponds to less than 1 sec, leass than 5 sec, less than 3 sec and less
			than 10 sec respectively.

		reliability:
			type int, reliability of the proxy, values can be 2500, 5000, 7500, 9000, 
			which correponds to more than 25%, more than 50%, more than 75% and more than 90 %
		


	Returns:
		list of proxies whose number will be equal to the number_of_proxies argument, depending upon the 
		availability of the proxies in the defined paramteres in the arguments

	"""
	def __init__(self, number_of_proxies, type_of_proxy, country, latency, reliability):
		self.arguments = lambda x: x if x else None
		self.number_of_proxies = self.arguments(number_of_proxies)
		self.type_of_proxy = self.arguments(type_of_proxy)
		self.country = self.arguments(country)
		self.latency = self.arguments(latency)
		self.reliability = self.arguments(latency)


	def xroxy_parse(self, html):
		return 



	def xroxy(self):
		driver = webdriver.Firefox()
		driver.get("http://www.xroxy.com/proxylist.htm")
		
		if self.type_of_proxy:
			self.select_option(driver, "//select[@id='type_id']", self.type_of_proxy)
		
		if self.country:
			self.select_option(driver, "//select[@id='country_id']", self.country)
		
		if self.latency:
			self.select_option(driver, "//select[@id='latency_id']", self.type_of_proxy)
		
		if self.reliability:
			self.select_option(driver, "//select[@id='type_id']", self.reliability)
		
		html = driver.page_source







	def select_option(self, driver, xpath, option):
		"""
		This method clicks on the webpage present on the selenium webdriver on the basis of the xpath of 
		the select option present on the dom of the webpage

		"""
		element = driver.find_element_by_xpath(xpath)
		p = Select(element)
		p.select_by_value(option)
		return
	

if __name__ == "__main__":
	instance = Proxies(number_of_proxies=10, type_of_proxy="Socks4", country="CN", latency=3000, reliability=9000)
	print instance.number_of_proxies
	print instance.type_of_proxy
	print instance.country
	print instance.latency
	print instance.reliability
	instance.xroxy()
