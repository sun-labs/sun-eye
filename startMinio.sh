#!/bin/bash

docker run -p 9000:9000\
  -e "MINIO_ACCESS_KEY=***REMOVED***" \
  -e "MINIO_SECRET_KEY=***REMOVED***" \
  -v /mnt/data:/data \
  -v /mnt/config:/root/.minio \
  minio/minio server /data