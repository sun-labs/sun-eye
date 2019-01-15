import cv2
import numpy as np

from lib.Frame import Frame
from lib.Display import Display

class SunEye():

    def __init__(self, args):
        self.nogui = args.nogui
        self.pf = None # previous frame
        self.initGUI()
        self.info = []
    
    def processFiles(self, files):
        for path in files:
            if "mp4" in path:
                self.pf = self.handleVideo(path)
            else:
                self.pf = self.handleImage(path)
                cv2.waitKey(0)
        return self.info

    def addInfo(self, info):
        print(info)
        self.info.append(info)
        return self.info
    
    def initGUI(self):
        if self.nogui is False:
            self.winm = Display('matches')
            self.winf = Display('features')
            self.wint = Display('trackers')
            self.wintresh = Display('tresh')

    def getFrameInfo(self, frame):
        info = frame.getCloudsInformation()
        del info["contours"]
        return info


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
        info = []
        while cap.isOpened():
            ret, frame = cap.read()
            if ret is True:
                cf = Frame(frame)
                self.drawFrame(cf, pf = pf)
                info = self.getFrameInfo(cf)
                self.addInfo(info)
                pf = cf
                if self.nogui is False:
                    cv2.waitKey(1)
                frame = cap.read()[1]
            else:
                break
        return pf

    def handleImage(self, path):
        frame = Frame(cv2.imread(path))
        self.drawFrame(frame)
        info = self.getFrameInfo(frame)
        self.addInfo(info)
        return frame, self.getFrameInfo(frame)