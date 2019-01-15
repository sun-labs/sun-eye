#!/usr/bin/env python3

import os
import cv2
import numpy as np
import sys
import argparse

from lib.Frame import Frame
from lib.Display import Display

class SunEye():

    def __init__(self, args):
        self.nogui = args.nogui
        self.pf = None # previous frame
        self.initGUI()
        self.processFiles(args.file_path)
    
    def processFiles(self, files):
        for path in files:
            if "mp4" in path:
                self.pf = self.handleVideo(path)
            else:
                self.pf = self.handleImage(path)
                cv2.waitKey(0)
    
    def initGUI(self):
        if self.nogui is False:
            self.winm = Display('matches')
            self.winf = Display('features')
            self.wint = Display('trackers')
            self.wintresh = Display('tresh')

    def getFrameInfo(self, frame):
        if self.pf is not None:
            matches = frame.matchWith(self.pf)
            cloudInfo = frame.getCloudsInformation()

    def drawFrame(self, frame, matches = None, pf = None):
        pf = self.pf if pf is None else pf # global previous frame if needed
        if self.nogui is False:
            self.winf.drawClouds(frame)
            self.wint.drawTrackpoints(frame)
            self.wintresh.imshow(frame.getTreshImage(frame.img))
            if pf is not None:
                matches = matches if matches is not None else frame.matchWith(pf)
                self.winm.drawMatches(frame, pf, matches)

    def handleVideo(self, path):
        cap = cv2.VideoCapture(path)
        pf = None # previous frame
        while cap.isOpened():
            ret, frame = cap.read()
            if ret is True:
                cf = Frame(frame)
                self.drawFrame(cf, pf = pf)
                    
                pf = cf
                cv2.waitKey(1)
                frame = cap.read()[1]
        return pf

    def handleImage(self, path):
        frame = Frame(cv2.imread(path))
        self.drawFrame(frame)
        return frame


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process weather information from frame / video.')
    parser.add_argument('file_path', metavar='FILE', type=str, nargs='+')
    parser.add_argument('--atemp')
    parser.add_argument('--ahumid')
    parser.add_argument('--nogui', default=False)
    args = parser.parse_args()
    
    
    se = SunEye(args)
    pf = None # previous frame
    