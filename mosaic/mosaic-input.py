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

# settings for each frame
W = 50
H = 25

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

def processFrame(frame):
    frame = cv2.resize(frame, (W, H))
    frame = frame.reshape(W*H, 3)
    return frame

def generateMosaic(path, args):
    if args.show_progress is True or args.show_finish is True:
        cv2.namedWindow('asdf')

    images = []
    if os.path.isfile(path): # video
        cap = cv2.VideoCapture(path)
        while cap.isOpened():
            ret, frame = cap.read()
            if ret is True:
                frame = processFrame(frame)
                images.append(frame)
            else:
                break
    else: # directory of images
        images = os.listdir(path)
        images.sort() # by filename
        for i in range(len(images)):
            frame = images[i]
            frame = processFrame(frame)
            images.append(frame)

    return images

def createMosaic(args = None, mc = None, date = None, input=None):
    if date is None and input is None:
        raise ValueError('One of START_DATE and --input has to be supplied. Exiting')

    if date is not None and (mc is None or args is None):
        raise ValueError('You need to supply minio / args if date supplied.')

    print(args)
    y, m, d = None, None, None
    if date is not None:
        y, m, d = parseDate(date)

    deviceName = args.device_name
    localPath = args.temp_dir if args.temp_dir is not None else './temp'
    localPath = '{}/{}-{}'.format(localPath, deviceName, date)
    savePath = args.output_dir if args.output_dir is not None else './mosaics'
    mcPath = '/{}/{}/{}/{}/'.format(deviceName, y, m, d)
    mpath = '{}/{}.jpg'.format(deviceName, date)

    minioMosaic = None
    if date is not None:
        # before doing all the hassle of downloading stuff
        # check if mosaic already available
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
    
    if input is None:
        # fetch images from minio
        photos = mc.list_objects_v2('***REMOVED***', mcPath)
        for p in photos:
            paths = p.object_name.split('/')
            filename = paths[len(paths) - 1]
            tempImg = '{}/{}'.format(localPath, filename)
            if not os.path.isfile(tempImg):
                print('dl [{}] ({}) {}'.format(deviceName, date, filename))
                mc.fget_object(p.bucket_name, p.object_name, tempImg)
        print('done downloading.')

    images = generateMosaic(input, args)
    imgCount = len(images)
    mimg = np.zeros((imgCount, W*H, 3))
    saveAt = '{}/{}-{}.jpg'.format(savePath, deviceName, date)

    for i in range(len(images)):
        img = images[i]
        print('{}% stitch {}'.format(math.floor((i/imgCount)*100), saveAt))
        mimg[i] = img
        if args.show_progress == True:
            cv2.imshow('asdf', convertToImage(mimg))
        

    if mimg is not None:
        if input is not None:
            paths = input.split('/')
            name = paths[len(paths) - 1]
            saveAt = '{}/{}.jpg'.format(savePath, name)
        cv2.imwrite(saveAt, mimg, [cv2.IMWRITE_JPEG_QUALITY, 100])
        print('mosaic done, saved in mosaics {}'.format(saveAt))

    if args.show_finish == True:
        cv2.imshow('asdf', convertToImage(mimg))
        cv2.waitKey(0) # last image

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
    parser.add_argument('date', metavar='START_DATE', type=str, nargs='?')
    parser.add_argument('--input', type=str, help='set folder or movie as input, skip download')
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
    
    mc = Minio('**HOST**',
                  access_key='**REMOVED**',
                  secret_key='**REMOVED**',
                  secure=False)

    if args.input is None:
        if args.end_date is not None: # range of dates
            sy, sm, sd = parseDate(args.date)
            ey, em, ed = parseDate(args.end_date)
            start_date = date(int(sy), int(sm), int(sd))
            end_date = date(int(ey), int(em), int(ed))
            for single_date in daterange(start_date, end_date):
                date = single_date.strftime("%Y-%m-%d")
                createMosaic(date=date, args=args, mc=mc)
        else: # single day
            createMosaic(date=args.date, args=args, mc=mc)
    else:
        createMosaic(input=args.input, args=args, mc=mc)

    exit()
    
