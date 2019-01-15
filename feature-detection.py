#!/usr/bin/env python3

import os
import cv2
import numpy as np
import sys

WIDTH = 640 
HEIGHT = 360
WIN_NAME = 'time variant'
WIN_NAME_B = 'features'
WIN_NAME_C = 'cloud info'
COLORS = [(128, 128, 0), (255, 0, 128), (0, 255, 255), (0, 255, 0)]

class Frame():
    def __init__(self, img):
        self.img = img
        self.pts = None
        self.kps = None
        self.ds = None
        self.lastMatches = None

    def getTreshImage(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ttype = cv2.THRESH_BINARY + cv2.THRESH_OTSU
        ret, thresh = cv2.threshold(gray, 0, 255, ttype)

        kernel = np.ones((3,3), np.uint8)
        bimg = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

        return bimg

    def getCloudsPercentage(self, img):
        pixels = img.flatten()
        count = len(pixels)
        white = len(pixels[pixels == 255])
        return white / count # done

    def getContours(self, img):
        return cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]

    def getCloudCount(self, img):
        contours = self.getContours(img)
        return len(list(filter(lambda x: len(x) > 30, contours)))

    def getCloudsInformation(self):
        bimg = self.getTreshImage(self.img)
        cloudyness = self.getCloudsPercentage(bimg)
        contours = self.getContours(bimg)
        nClouds = self.getCloudCount(bimg)

        return {
            "cloudyness": cloudyness,
            "contours": contours,
            "cloudCount": nClouds
        }

    # find keypoints from one image to the next
    def matchWith(self, frame):
        # Initiate SIFT detector
        orb = cv2.ORB_create()
        img1 = self.img.copy()
        img2 = frame.img.copy()
        kp1, des1 = orb.detectAndCompute(img1, None)
        kp2, des2 = orb.detectAndCompute(img2, None)

        self.setKps(kp1)
        self.setDs(des1)
        frame.setKps(kp2)
        frame.setDs(des2)

        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        self.lastMatches = bf.match(des1, des2)
        img3 = None
        img3 = cv2.drawMatches(img1, kp1, img2, kp2, self.lastMatches[:], flags=2, outImg=img3)
        return img3


    def setPts(self, pts):
        self.pts = pts

    def setKps(self, kps):
        self.kps = kps
    
    def setDs(self, ds):
        self.ds = ds


def processImage(img):
    img = img.copy()
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

def processClouds(img, frame, pc=None, pl=None):

    frame = frame or Frame(img)
    info = frame.getCloudsInformation()
    for cnt in info["contours"]:
        cv2.drawContours(img,[cnt],0,(0,0,255),2)

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, '{} clouds'.format(info["cloudCount"]),(10,500), font, 4,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(img, '{}% cloudy'.format(round(info["cloudyness"] * 100)), (10, 300), font, 2, cv2.LINE_AA)

    return img

def processClouds_kmeans(img, frame, pc = None, pl = None):
    img = cv2.resize(img, (WIDTH, HEIGHT))
    
    pts = frame.pts
    K = 4
    flags = cv2.KMEANS_RANDOM_CENTERS
    if pc is not None and pl is not None:
      print(len(pc), len(pl), K, len(pts))
    if pl is not None:
        if len(pl) > len(pts):
            pl = pl[:len(pts)]
        else:
            pl = np.pad(pl, len(pts), 'constant')

    (ret, label, centroid) = cv2.kmeans(pts, K, None, (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 5, 1.0), 5, flags)
    centroid = np.uint8(centroid)
    res = centroid[label.flatten()]
    print(centroid, len(centroid))
    for i1 in range(len(res)):
        p = pts[i1].flatten()
        color = COLORS[int(label[i1])]
       #  print(p)
        u1, v1 = (int(round(p[0])), int(round(p[1])))
        cv2.circle(img, (u1, v1), 3, color)

    return img, None, centroid, label


def initWindow():
    cv2.namedWindow(WIN_NAME, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WIN_NAME, WIDTH, HEIGHT)
    cv2.namedWindow(WIN_NAME_B, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WIN_NAME_B, WIDTH, HEIGHT)
    cv2.namedWindow(WIN_NAME_C, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WIN_NAME_C, WIDTH, HEIGHT)


if __name__ == "__main__":

    initWindow()
    cap = cv2.VideoCapture(sys.argv[1])
    
    pf = None #previous frame
    pc = None #previous centroids kmeans
    pl = None # previous kmeans labels
    while cap.isOpened():
        ret, frame = cap.read()
        if ret is True:
            img, cf = processImage(frame)
            img = img.copy()
            imgCloud = processClouds(frame, cf, pc, pl)

            cv2.imshow(WIN_NAME_C, imgCloud)
            cv2.imshow(WIN_NAME_B, img)
            if pf is not None:
                img = cf.matchWith(pf)
            pf = cf
            cv2.imshow(WIN_NAME, img)
            cv2.waitKey(1)
            success, img = cap.read()
        else:
            break