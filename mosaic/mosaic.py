#!/usr/bin/env python3

import sys, os
import minio
import shutil
from minio import Minio
from minio.error import ResponseError
import argparse
import cv2
import numpy as np
import math
from datetime import timedelta, date, datetime as dt

def parseDate(dateStr):
    return tuple(dateStr.split("-"))

def convertToImage(arr):
    new = np.zeros(arr.shape)
    new[:, :, 0] = arr[:, :, 0] / 255.0
    new[:, :, 1] = arr[:, :, 1] / 255.0
    new[:, :, 2] = arr[:, :, 2] / 255.0
    return new

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)

def createMosaic(date, args, mc):
    print(args)
    y, m, d = parseDate(date)

    deviceName = args.device_name
    localPath = args.temp_dir if args.temp_dir is not None else './temp'
    localPath = '{}/{}-{}'.format(localPath, deviceName, date)
    savePath = args.output_dir if args.output_dir is not None else './mosaics'
    mcPath = '/{}/{}/{}/{}/'.format(deviceName, y, m, d)
    mpath = '{}/{}.jpg'.format(deviceName, date)

    # before doing all the hassle of downloading stuff
    # check if mosaic already available
    minioMosaic = None
    if args.no_upload is False:
        print("checking if mosaic exists")
        try:
            minioMosaic = mc.stat_object('sky-mosaics', mpath)
        except minio.error.NoSuchKey:
            print("no mosaic in bucket, continuing..")

        if minioMosaic is not None and args.force is False: # already exists skip
            print("SKIP mosaic already exists in bucket, NEXT.")
            return

    os.makedirs(localPath, exist_ok=True)
    os.makedirs(savePath, exist_ok=True)
    
    # fetch images from minio
    photos = mc.list_objects_v2('sky-photos', mcPath)
    for p in photos:
        paths = p.object_name.split('/')
        filename = paths[len(paths) - 1]
        tempImg = '{}/{}'.format(localPath, filename)
        if not os.path.isfile(tempImg):
            print('dl [{}] ({}) {}'.format(deviceName, date, filename))
            mc.fget_object(p.bucket_name, p.object_name, tempImg)
    print('done downloading.')

    if args.show_progress is True or args.show_finish is True:
        cv2.namedWindow('asdf')
    images = os.listdir(localPath)
    images.sort() # by filename
    imgCount = len(images)

    W = 50
    H = 25
    mimg = np.zeros((imgCount, W*H, 3))
    saveAt = '{}/{}-{}.jpg'.format(savePath, deviceName, date)

    # make mosaic
    if (not os.path.isfile(saveAt) and imgCount > 0) or args.force is True:
        print('mosaic in progress...')
        for i in range(imgCount):
            print('{}% stitch {}'.format(math.floor((i/imgCount)*100), saveAt))
            img = images[i]
            cv2.waitKey(1)
            imgPath = "{}/{}".format(localPath, img)
            img = cv2.imread(imgPath)
            if img is None or len(img) == 0:
                continue
            rimg = cv2.resize(img, (W, H))
            rimg = rimg.reshape(W*H, 3)
            mimg[i] = rimg
            if args.show_progress == True:
                cv2.imshow('asdf', convertToImage(mimg))
        
        if args.show_finish == True:
            cv2.imshow('asdf', convertToImage(mimg))
            cv2.waitKey(0) # last image

        if mimg is not None:
            cv2.imwrite(saveAt, mimg, [cv2.IMWRITE_JPEG_QUALITY, 100])
            print('mosaic done, saved in mosaics {}'.format(saveAt))
    else:
        print("no images found, next..")

    if args.save_temp is False:
        print("time to clean up")
        shutil.rmtree(localPath)

    # upload to minio
    if not args.no_upload:
        if os.path.isfile(saveAt):
            mfilename = date
            if minioMosaic is None or args.force is True:
                print('upload mosaic to minio bucket {}'.format(mpath))
                etag = mc.fput_object('sky-mosaics', mpath, saveAt)
                if etag is not None:
                    print("upload sucessful!")
                else:
                    print("failed upload..")
            else:
                print("[SKIP] {} already exists in bucket.".format(mpath))
        else:
            print("no mosaic to upload at {}".format(saveAt))

    cv2.destroyAllWindows()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Generate mosaic from weather photos')
    parser.add_argument('date', metavar='START_DATE', type=str)
    parser.add_argument('--end-date', type=str, help='Iterate this date')
    parser.add_argument('--device-name', type=str)
    parser.add_argument('--show-finish', action='store_true')
    parser.add_argument('--show-progress', action='store_true')
    parser.add_argument('--save-temp', action='store_true')
    parser.add_argument('--no-upload', action='store_true')
    parser.add_argument('--force', action='store_true')
    parser.add_argument('--output-dir', type=str)
    parser.add_argument('--temp-dir', type=str)
    args = parser.parse_args()
    
    mc = Minio('**MINIO_HOST**',
                  access_key='**REMOVED**',
                  secret_key='**REMOVED**',
                  secure=False)

    if args.end_date is not None: # range of dates
        sy, sm, sd = parseDate(args.date)
        ey, em, ed = parseDate(args.end_date)
        start_date = date(int(sy), int(sm), int(sd))
        end_date = date(int(ey), int(em), int(ed))
        for single_date in daterange(start_date, end_date):
            date = single_date.strftime("%Y-%m-%d")
            createMosaic(date, args, mc)
    else: # single day
        createMosaic(args.date, args, mc)

    exit()
    
