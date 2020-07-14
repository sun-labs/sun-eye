#!/usr/bin/env python

import boto
import sys, os
from minio import Minio
from minio.error import ResponseError

minioClient = Minio('**REMOVED**',
                  access_key='**REMOVED**',
                  secret_key='**REMOVED**',
                  secure=False)


DOWNLOAD_LOCATION_PATH = os.path.expanduser("~") + "**REMOVED**"
if not os.path.exists(DOWNLOAD_LOCATION_PATH):
	print ("Making download directory")
	os.mkdir(DOWNLOAD_LOCATION_PATH)


def backup_s3_folder():
	BUCKET_NAME = "**REMOVED**"
	# AWS_ACCESS_KEY_ID= os.getenv("AWS_KEY_ID") # set your AWS_KEY_ID  on your environment path
	# AWS_ACCESS_SECRET_KEY = os.getenv("AWS_ACCESS_KEY") # set your AWS_ACCESS_KEY  on your environment path
	bucket = minioClient.list_objects(BUCKET_NAME, recursive=True)

	for l in bucket:
		key_string = str(l.object_name)
		s3_path = DOWNLOAD_LOCATION_PATH + key_string # NOTE this is the path where the data will end up on our computer
		# try:
		print ("Current File is ", s3_path)

		try:
				minioClient.fget_object(BUCKET_NAME, l.object_name, s3_path)
				# minioClient.remove_object(BUCKET_NAME, l.object_name) # NOTE uncomment this to remove the img when we download
		except ResponseError as err:
				print(err)



if __name__ == '__main__':
	backup_s3_folder()