#!/usr/bin/env python3

import os
import cv2
import numpy as np
import sys

WIDTH = 640 
HEIGHT = 360
WIN_NAME = 'image'
WIN_NAME_B = 'features'

class Frame():
    def __init__(self, img):
        self.img = img
        self.pts = None
        self.kps = None
        self.ds = None

    def setPts(self, pts):
        self.pts = pts

    def setKps(self, kps):
        self.kps = kps
    
    def setDs(self, ds):
        self.ds = ds


def processImage(img):
    frame = Frame(img)
    img = cv2.resize(img, (WIDTH, HEIGHT))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    points = cv2.goodFeaturesToTrack(gray, 300, 0.01, 10)
    frame.setPts(points)
    # print(points)
    for i1 in range(len(points)):
        p = points[i1][0]
        u1, v1 = int(round(p[0])), int(round(p[1]))
        cv2.circle(img, (u1, v1), color=(0, 255, 0), radius=3)

    return img, frame

def match_frames(f1, f2):
    # Initiate SIFT detector
    orb = cv2.ORB_create()
    img1 = f1.img
    img2 = f2.img
    kp1, des1 = orb.detectAndCompute(f1.img,None)
    kp2, des2 = orb.detectAndCompute(f2.img,None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1,des2)
    img3 = None
    img3 = cv2.drawMatches(img1,kp1,img2,kp2,matches[:], flags=2, outImg=img3)
    return img3




def initWindow():
    cv2.namedWindow(WIN_NAME, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WIN_NAME, WIDTH, HEIGHT)
    cv2.namedWindow(WIN_NAME_B, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WIN_NAME_B, WIDTH, HEIGHT)


if __name__ == "__main__":

    initWindow()
    cap = cv2.VideoCapture(sys.argv[1])
    
    pf = None#previous frame
    while cap.isOpened():
        ret, frame = cap.read()
        if ret is True:
            img, cf = processImage(frame)
            cv2.imshow(WIN_NAME_B, img)
            if pf is not None:
                img = match_frames(cf, pf)
            pf = cf
            cv2.imshow(WIN_NAME, img)
            cv2.waitKey(1)
            success, img = cap.read()
        else:
            break