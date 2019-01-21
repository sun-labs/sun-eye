#!/usr/bin/env python3

import sys, os
from minio import Minio
from minio.error import ResponseError
import argparse
import cv2
import numpy as np
import math

def parseDate(dateStr):
    return tuple(dateStr.split("-"))

def convertToImage(arr):
    new = np.zeros(arr.shape)
    new[:, :, 0] = arr[:, :, 0] / 255.0
    new[:, :, 1] = arr[:, :, 1] / 255.0
    new[:, :, 2] = arr[:, :, 2] / 255.0
    return new

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Generate mosaic from weather photos')
    parser.add_argument('date', metavar='DATE', type=str)
    parser.add_argument('--device-name', type=str)
    parser.add_argument('--show-finish', action='store_true')
    parser.add_argument('--show-progress', action='store_true')
    args = parser.parse_args()
    
    mc = Minio('***REMOVED***',
                  access_key='***REMOVED***',
                  secret_key='***REMOVED***',
                  secure=False)
    date = args.date
    y, m, d = parseDate(date)

    deviceName = args.device_name
    localPath = './temp/{}-{}'.format(deviceName, date)
    savePath = './mosaics'
    mcPath = '/{}/{}/{}/{}/'.format(deviceName, y, m, d)

    os.makedirs(localPath, exist_ok=True)
    os.makedirs(savePath, exist_ok=True)
    
    photos = mc.list_objects_v2('***REMOVED***', mcPath)
    for p in photos:
        paths = p.object_name.split('/')
        filename = paths[len(paths) - 1]
        tempImg = '{}/{}'.format(localPath, filename)
        if not os.path.isfile(tempImg):
            mc.fget_object(p.bucket_name, p.object_name, tempImg)
            print(filename)
    print('done downloading.')

    cv2.namedWindow('asdf')
    images = os.listdir(localPath)
    images.sort() # by filename
    imgCount = len(images)

    W = 50
    H = 25
    mimg = np.zeros((imgCount, W*H, 3))

    print('mosaic in progress...')
    for i in range(imgCount):
        print('{}% {}/{}'.format(math.floor((i/imgCount)*100), i, imgCount))
        img = images[i]
        cv2.waitKey(1)
        imgPath = "{}/{}".format(localPath, img)
        img = cv2.imread(imgPath)
        rimg = cv2.resize(img, (W, H))
        rimg = rimg.reshape(W*H, 3)
        mimg[i] = rimg
        if args.show_progress == True:
            cv2.imshow('asdf', convertToImage(mimg))
    
    if args.show_finish == True:
        cv2.imshow('asdf', convertToImage(mimg))
        cv2.waitKey(0) # last image

    cv2.imwrite('{}/{}-{}.jpg'.format(savePath, deviceName, date), mimg, [cv2.IMWRITE_JPEG_QUALITY, 100])
    print('mosaic done, saved in mosaics')

