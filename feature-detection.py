#!/usr/bin/env python3

import os
import cv2
import numpy as np
import sys
import argparse

from lib.Frame import Frame
from lib.Display import Display

def parseFrame(frame):
    cf = Frame(frame)
    winf.drawClouds(cf)
    wint.drawTrackpoints(cf)
    wintresh.imshow(cf.getTreshImage(cf.img))
    return cf

def parseVideo(path):
    cap = cv2.VideoCapture(args.file_path)
    winm = Display('matches')
    pf = None # previous frame
    while cap.isOpened():
        ret, frame = cap.read()
        if ret is True:
            cf = parseFrame(frame)
            if pf is not None:
                matches = cf.matchWith(pf)
                winm.drawMatches(cf, pf, matches)
            pf = cf
            cv2.waitKey(1)
            frame = cap.read()[1]

def parseImage(path):
    frame = cv2.imread(path)
    cf = parseFrame(frame)
    cv2.waitKey(0)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process weather information from frame / video.')
    parser.add_argument('file_path', metavar='FILE', type=str)
    parser.add_argument('--atemp')
    parser.add_argument('--ahumid')
    args = parser.parse_args()

    winf = Display('features')
    wint = Display('trackers')
    wintresh = Display('tresh')

    path = args.file_path
    if "mp4" in path:
        parseVideo(path)
    else:
        parseImage(path)