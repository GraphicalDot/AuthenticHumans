#-*- coding: utf-8 -*-

"""
This module deals with all the storage of the objects be it on google cloud storage, redis, mongodb 
"""

from gcs_storage import GCS
from redis_storage import RedisProxy
from redis_storage import RedisUrlWorkers

