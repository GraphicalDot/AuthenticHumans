#-*- coding: utf-8 -*-
import boto
import gcs_oauth2_boto_plugin
import os
import shutil
import StringIO
import tempfile
import time
import hashlib
import StringIO
# URI scheme for Google Cloud Storage.
GOOGLE_STORAGE = 'gs'
# URI scheme for accessing local files.
LOCAL_FILE = 'file'

# Fallback logic. In https://console.developers.google.com
# under Credentials, create a new client ID for an installed application.
# Required only if you have not configured client ID/secret in
# the .boto file or as environment variables.
CLIENT_ID = '690199257268-vf4hl7ap9rsc5nau19nouacp83f69j0e.apps.googleusercontent.com'
CLIENT_SECRET = 'eJS6bN5Ovxb_SXN4OjQQNglx'
BUCKET_NAME = 'testing-stage1-RDD'
PROJECT_ID = 'project-amoeba-testing'



class GCS:
	"""
	This is the class that will be used to create new bucket, uploading object on gcs 
	and generating url after saving the object
	"""
	gcs_oauth2_boto_plugin.SetFallbackClientIdAndSecret(CLIENT_ID, CLIENT_SECRET)
	
	def __init__(self, filename=None, html_string=None, bucket_name=None, url=None):
		self.html_string = html_string
		self.bucket_name = bucket_name
		if not filename:
			self.filename = hashlib.sha1(self.html_string.encode("utf-8")).hexdigest()
		else:
			self.filename = filename
		self.uri = boto.storage_uri(self.bucket_name, GOOGLE_STORAGE)
		self.header_values = {"x-goog-project-id": PROJECT_ID}

	def create_bucket(self):
		"""
		This method creates a bucket, if bucket doesnt exists

		"""
		# Try to create the bucket.
		try:
			self.uri.create_bucket(headers=self.header_values)
			print 'Successfully created bucket "%s"'%self.bucket_name
			return (True, None)

		except boto.exception.GSCreateError, e:
			print 'Bucket already exists'
			return (True, None)
		
		except boto.exception.StorageCreateError, e:
			print 'Failed to create bucket:', e
			return (False, e)

		except gcs_oauth2_boto_plugin.oauth2_client.AccessTokenRefreshError as e:
			print "invalid client:", e
			return (False, e)
		except Exception as e:
			return (False, e)

	def upload_file(self):
		destination_uri = boto.storage_uri(self.bucket_name + '/' + self.filename + '.html', GOOGLE_STORAGE)
		destination_uri.new_key().set_contents_from_string(self.html_string)
		return "%s.html"%self.filename 

	def download_file(self):
		"""
		This method return the file object present on the filename on the bucket
		"""
		src_uri = boto.storage_uri(self.bucket_name + '/' + self.filename, GOOGLE_STORAGE)
		object_contents = StringIO.StringIO()
		src_uri.get_key().get_file(object_contents)
		object_contents.seek(0)
		result = object_contents.read()
		object_contents.close()
		return result

	def delete_file(self):
		"""
		This method delete the file object present on the filename on the bucket
		"""
		src_uri = boto.storage_uri(self.bucket_name + '/' + self.filename, GOOGLE_STORAGE)
		try:
			src_uri.delete_key()
			return True
		except Exception as e:
			print e
			return False



