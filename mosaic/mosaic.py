#!/usr/bin/env python3

import boto
import sys, os
from minio import Minio
from minio.error import ResponseError

mc = Minio('***REMOVED***',
                  access_key='***REMOVED***',
                  secret_key='***REMOVED***',
                  secure=False)