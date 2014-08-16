#!/usr/bin/env python
#-*- coding: utf-8 -*-


import boto
import gcs_oauth2_boto_plugin
import os
import shutil
import StringIO
import tempfile
import time

# URI scheme for Google Cloud Storage.
GOOGLE_STORAGE = 'gs'
# URI scheme for accessing local files.
LOCAL_FILE = 'file'

# Fallback logic. In https://console.developers.google.com
# under Credentials, create a new client ID for an installed application.
# Required only if you have not configured client ID/secret in
# the .boto file or as environment variables.
CLIENT_ID = '690199257268-nmjkfa8d4jdb6mnfllkqsq6a7mc62v05.apps.googleusercontent.com'
CLIENT_SECRET = '5IR9oQ3L1j4WsRnwxL7I6vXA'
BUCKET_NAME = 'testing-stage1-rdd'
PROJECT_ID = 'project-amoeba-testing'



def create_bucket():
	gcs_oauth2_boto_plugin.SetFallbackClientIdAndSecret(CLIENT_ID, CLIENT_SECRET)
	uri = boto.storage_uri(BUCKET_NAME, GOOGLE_STORAGE)
	# Try to create the bucket.
	try:
		header_values = {"x-goog-project-id": PROJECT_ID}
		uri.create_bucket(headers=header_values)
		print 'Successfully created bucket "%s"' % name
	except boto.exception.StorageCreateError, e:
		print 'Failed to create bucket:', e
	except gcs_oauth2_boto_plugin.oauth2_client.AccessTokenRefreshError as e:
		print "invalid client:", e






if __name__ == "__main__":
	create_bucket()


