#!/usr/bin/env python3

import os
import cv2
import numpy as np
import sys

WIDTH = 640 
HEIGHT = 360
WIN_NAME = 'image'

def processImage(img):
    img = cv2.resize(img, (WIDTH, HEIGHT))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    points = cv2.goodFeaturesToTrack(gray, 25, 0.01, 10)
    # print(points)
    for i1 in range(len(points)):
        p = points[i1][0]
        u1, v1 = int(round(p[0])), int(round(p[1]))
        cv2.circle(img, (u1, v1), color=(0, 255, 0), radius=3)

    return img



def initWindow():
    cv2.namedWindow(WIN_NAME, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WIN_NAME, WIDTH, HEIGHT)


if __name__ == "__main__":

    initWindow()
    cap = cv2.VideoCapture(sys.argv[1])
    
    while cap.isOpened():
        ret, frame = cap.read()
        if ret is True:
            img = processImage(frame)
            cv2.imshow(WIN_NAME, img)
            cv2.waitKey(1)
            success, img = cap.read()
        else:
            break