#!/usr/bin/env python3

import sys, os
from minio import Minio
from minio.error import ResponseError
import argparse
import cv2
import numpy as np

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
        tempImg = '{}/{}'.format(localPath, filename)
        if not os.path.isfile(tempImg):
            mc.fget_object(p.bucket_name, p.object_name, tempImg)
            print(filename)
    print('done downloading.')


    mimg = []

    cv2.namedWindow('asdf')
    images = os.listdir(localPath)
    images.sort()
    for img in images:
        cv2.waitKey(1)
        imgPath = "{}/{}".format(localPath, img)
        img = cv2.imread(imgPath)
        rimg = cv2.resize(img, (50, 25))
        mimg.append(rimg.reshape(50 * 25, -1))
        cv2.imshow('asdf', np.array(mimg))
    cv2.waitKey(0)