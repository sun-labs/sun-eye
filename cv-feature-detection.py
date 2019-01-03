#!/usr/bin/env python3

import os
import cv2
import numpy as np
import sys

def processImage(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    points = cv2.goodFeaturesToTrack(gray, 25, 0.01, 10)


if __name__ == "__main__":

    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.waitKey(0)

    cv2.VideoCapture(sys.argv[1])