#!/usr/bin/env python
from datetime import datetime
from time import sleep
import picamera
import os
import yaml
import datetime
from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)

# Initialize minioClient with an endpoint and access/secret keys.
minioClient = Minio('***REMOVED***',
                    access_key='***REMOVED***',
                    secret_key='***REMOVED***',
                    secure=False)


# testing
with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

# photo props
image_width = cfg['image_settings']['horizontal_res']
image_height = cfg['image_settings']['vertical_res']
file_extension = cfg['image_settings']['file_extension']
photo_interval = cfg['image_settings']['photo_interval'] # Interval between photo (in seconds)
image_folder = cfg['image_settings']['folder_name']

# camera setup
camera = picamera.PiCamera()
camera.resolution = (image_width, image_height)
camera.awb_mode = cfg['image_settings']['awb_mode']

# verify image folder exists and create if it does not
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

# camera warm-up time
sleep(2)

# endlessly capture images awwyiss
while True:
    # Build filename string
    filename = str(datetime.datetime.utcnow().replace(microsecond=0)) + file_extension
    filepath = image_folder + '/' + filename

    if cfg['debug'] == True:
        print ('[debug] Taking photo and saving to path ' + filepath)

    # Take Photo
    camera.capture(filepath)

    if cfg['debug'] == True:
        print ('[debug] Uploading ' + filepath + ' to s3')

    # Upload to S3
    conn = minioClient.fput_object('***REMOVED***', filename, filepath)

    # Cleanup
    if os.path.exists(filepath):
        os.remove(filepath)

    # sleep
    sleep(photo_interval)