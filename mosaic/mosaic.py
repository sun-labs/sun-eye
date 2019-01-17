#!/usr/bin/env python3

import sys, os
from minio import Minio
from minio.error import ResponseError
import argparse
import cv2

def parseDate(dateStr):
    return tuple(dateStr.split("-"))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Generate mosaic from weather photos')
    #parser.add_argument('--date', type=str)
    #parser.add_argument('--end', type=str)
    parser.add_argument('date', metavar='DATE', type=str)
    args = parser.parse_args()
    
    mc = Minio('***REMOVED***',
                  access_key='***REMOVED***',
                  secret_key='***REMOVED***',
                  secure=False)

    y, m, d = parseDate(args.date)

    localPath = './temp/{}'.format(args.date)
    mcPath = '/***REMOVED***/{}/{}/{}/'.format(y, m, d)

    os.makedirs(localPath, exist_ok=True)

    photos = mc.list_objects_v2('***REMOVED***', mcPath)
    for p in photos:
        paths = p.object_name.split('/')
        filename = paths[len(paths) - 1]
        mc.fget_object(p.bucket_name, p.object_name, '{}/{}'.format(localPath, filename))
        print(filename)

    # print(dir(photos))
    # for photo in photos:
        # print(photo)
    # print(len(photos))
    # print(dir(buckets))