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

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Generate mosaic from weather photos')
    #parser.add_argument('--date', type=str)
    #parser.add_argument('--end', type=str)
    parser.add_argument('date', metavar='DATE', type=str)
    parser.add_argument('--device-name', type=str)
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
    images.sort()
    imgCount = len(images)

    W = 50
    H = 25
    #mimg = np.arange(0, 50*25*imgCount*3).reshape(imgCount, 50*25, -1)
    mimg = np.zeros((imgCount, W*H, 3))
    # print(mimg)

    print('mosaic in progress...')
    for i in range(imgCount):
        print('{}% {}/{}'.format(math.floor((i/imgCount)*100), i, imgCount))
        img = images[i]
        cv2.waitKey(1)
        imgPath = "{}/{}".format(localPath, img)
        img = cv2.imread(imgPath)
        rimg = cv2.resize(img, (W, H))
        rimg = rimg.reshape(W*H, 3)
        # print(len(rimg), len(mimg[i]))
        mimg[i] = rimg
        mimg[i, :, 0] = mimg[i, :, 0] / 255.0
        mimg[i, :, 1] = mimg[i, :, 1] / 255.0
        mimg[i, :, 2] = mimg[i, :, 2] / 255.0
        
        # cv2.imshow('asdf', mimg)

    cv2.imwrite('{}/{}-{}.jpg'.format(savePath, deviceName, date), mimg)
    print('mosaic done, saved in mosaics')
    cv2.waitKey(0) # last image

