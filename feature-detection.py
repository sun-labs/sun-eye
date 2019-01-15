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
        self.img = self.preprocess(img)
        self.pts = None
        self.kps = None
        self.ds = None
        self.lastMatches = None # from BFMatcher

    def preprocess(self, img):
        img = cv2.resize(img, (WIDTH, HEIGHT))
        return img


    def getTreshImage(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ttype = cv2.THRESH_BINARY + cv2.THRESH_OTSU
        thresh = cv2.threshold(gray, 0, 255, ttype)[1]

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

    def getCloudCount(self, img, contours = None):
        if contours is None:
            contours = self.getContours(img)
        return len(list(filter(lambda x: len(x) > 30, contours)))

    def getCloudsInformation(self):
        bimg = self.getTreshImage(self.img)
        cloudyness = self.getCloudsPercentage(bimg)
        contours = self.getContours(bimg)
        nClouds = self.getCloudCount(bimg, contours=contours)

        return {
            "cloudyness": cloudyness,
            "contours": contours,
            "cloudCount": nClouds
        }

    def getTrackPoints(self):
        img = self.img.copy()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        points = cv2.goodFeaturesToTrack(gray, 300, 0.01, 10)
        self.setPts(points)
        return points

    # find keypoints from one image to the next
    def matchWith(self, frame):
        # Initiate SIFT detector
        orb = cv2.ORB_create()
        img1 = self.img.copy()
        img2 = frame.img.copy()
        kp1, des1 = orb.detectAndCompute(img1, None)
        kp2, des2 = orb.detectAndCompute(img2, None)

        self.setKps(kp1)
        self.setDes(des1)
        frame.setKps(kp2)
        frame.setDes(des2)

        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        self.lastMatches = bf.match(des1, des2)
        return self.lastMatches



    def setPts(self, pts):
        self.pts = pts

    def setKps(self, kps):
        self.kps = kps
    
    def setDes(self, des):
        self.des = des


def drawTrackpoints(frame):
    points = frame.getTrackPoints()
    img = frame.img.copy()
    for i1 in range(len(points)):
        p = points[i1][0]
        u1, v1 = int(round(p[0])), int(round(p[1]))
        cv2.circle(img, (u1, v1), color=(0, 255, 0), radius=3)

    return img

def drawMatches(f1, f2, matches):
    img3 = None
    return cv2.drawMatches(f1.img, f1.kps, f2.img, f2.kps, matches[:], flags=2, outImg=img3)

def drawClouds(frame):

    info = frame.getCloudsInformation()
    img = frame.img.copy()
    for cnt in info["contours"]:
        cv2.drawContours(img,[cnt],0,(0,0,255),2)

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, '{} clouds'.format(info["cloudCount"]), (10, 100), font, 1, cv2.LINE_AA)
    cv2.putText(img, '{}% cloudy'.format(round(info["cloudyness"] * 100)), (10, 300), font, 2, cv2.LINE_AA)

    return img


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
    while cap.isOpened():
        ret, frame = cap.read()
        if ret is True:
            cf = Frame(frame)
            imgCloud = drawClouds(cf)
            imgTrack = drawTrackpoints(cf)

            if pf is not None:
                matches = cf.matchWith(pf)
                imgMatch = drawMatches(cf, pf, matches)
                cv2.imshow(WIN_NAME, imgMatch)

            cv2.imshow(WIN_NAME_C, imgCloud)
            cv2.imshow(WIN_NAME_B, imgTrack)
            
            pf = cf
            cv2.waitKey(1)
            success, frame = cap.read()
        else:
            break