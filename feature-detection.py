#!/usr/bin/env python3

import os
import cv2
import numpy as np
import sys

from lib.Frame import Frame
from lib.Display import Display

if __name__ == "__main__":

    cap = cv2.VideoCapture(sys.argv[1])

    winf = Display('features')
    winm = Display('matches')
    wint = Display('trackers')
    wintresh = Display('tresh')
    
    pf = None #previous frame
    while cap.isOpened():
        ret, frame = cap.read()
        if ret is True:
            cf = Frame(frame)
            winf.drawClouds(cf)
            wint.drawTrackpoints(cf)
            wintresh.imshow(cf.getTreshImage(cf.img))

            if pf is not None:
                matches = cf.matchWith(pf)
                winm.drawMatches(cf, pf, matches)

            pf = cf

            cv2.waitKey(1)
            success, frame = cap.read()
        else:
            break