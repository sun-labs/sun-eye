import cv2
import numpy as np

import config

class Frame():
    def __init__(self, img):
        self.img = self.preprocess(img)
        self.pts = None
        self.kps = None
        self.ds = None
        self.lastMatches = None # from BFMatcher

    def preprocess(self, img):
        img = cv2.resize(img, (config.WIDTH, config.HEIGHT))
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