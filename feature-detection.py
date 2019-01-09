#!/usr/bin/env python3

import os
import cv2
import numpy as np
import sys

WIDTH = 640 
HEIGHT = 360
WIN_NAME = 'image'
WIN_NAME_B = 'features'
WIN_NAME_C = 'clouds'
COLORS = [(128, 128, 0), (255, 0, 128), (0, 255, 255), (0, 255, 0)]

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

def processClouds(img, frame, pc=None, pl=None):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ttype = cv2.THRESH_BINARY + cv2.THRESH_OTSU
    ret, thresh = cv2.threshold(gray, 0, 255, ttype)

    kernel = np.ones((3,3), np.uint8)
    bimg = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

    # img = cv2.Canny(bimg, 1, 1)

    contours,h = cv2.findContours(bimg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        cv2.drawContours(img,[cnt],0,(0,0,255),2)


   #  print(list(map(lambda x: len(x), contours)))

    clouds = len(list(filter(lambda x: len(x) > 30, contours)))
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img,str(clouds),(10,500), font, 4,(255,255,255),2,cv2.LINE_AA)
    # img = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE, (0,0))
    # lines = cv2.HoughLines(opening, np.pi/180, 80, 30, 10)

    # if lines is not None:
    #     for i1 in range(len(lines)):
    #         x, y = lines[i1]
    #         img = cv2.line(img, x, y, (255, 0, 0))

    #img, contours, h = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    #markers = cv2.connectedComponents(opening)
    #markers = cv2.watershed(img)

    #sure_bg = cv2.dilate(opening, kernel, iterations=2)

    #dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)

    #ret, sure_fg = cv2.threshold(dist_transform, 5, 255, cv2.THRESH_BINARY_INV)
    #sure_fg = np.uint8(sure_fg)

    #unknown = cv2.subtract(np.zeros(len(sure_fg)), sure_fg)

    #ret, markers = cv2.connectedComponents(sure_fg)
    #markers = markers+ 1
    #markers[unknown == 255] = 0

    # cv2.applyColorMap(markers, cv2.COLORMAP_AUTUMN)

    #markers = cv2.watershed(img, markers)
    # img[markers == -1] = [255, 128, 0]

    return img, None, None, None

def processClouds_kmeans(img, frame, pc = None, pl = None):
    img = cv2.resize(img, (WIDTH, HEIGHT))
    
    # print(frame.pts)
    pts = frame.pts
    #Z = pts.reshape(-1, 2)
    #Z = Z.flatten()
    # print(Z)
    #print(pc, pl)
    #print(len(pts), len(pl))
    K = 4
    flags = cv2.KMEANS_RANDOM_CENTERS
    if pc is not None and pl is not None:
      print(len(pc), len(pl), K, len(pts))
    if pl is not None:
        #flags = cv2.KMEANS_USE_INITIAL_LABELS
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
            imgCloud, cfCloud, centroids, labels = processClouds(frame, cf, pc, pl)
            pc = centroids
            pl = labels
            cv2.imshow(WIN_NAME_C, imgCloud)
            cv2.imshow(WIN_NAME_B, img)
            if pf is not None:
                img = match_frames(cf, pf)
            pf = cf
            cv2.imshow(WIN_NAME, img)
            cv2.waitKey(1)
            success, img = cap.read()
        else:
            break