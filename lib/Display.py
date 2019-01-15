import cv2

import config

class Display():

    def __init__(self, name, w = config.WIDTH, h = config.HEIGHT):

        self.name = name
        cv2.namedWindow(name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(name, w, h)

    def imshow(self, img):
        cv2.imshow(self.name, img)


    def drawTrackpoints(self, frame):
        points = frame.getTrackPoints()
        img = frame.img.copy()
        for i1 in range(len(points)):
            p = points[i1][0]
            u1, v1 = int(round(p[0])), int(round(p[1]))
            cv2.circle(img, (u1, v1), color=(0, 255, 0), radius=3)

        self.imshow(img)

    def drawMatches(self, f1, f2, matches):
        img3 = None
        self.imshow(cv2.drawMatches(f1.img, f1.kps, f2.img, f2.kps, matches[:], flags=2, outImg=img3))

    def drawClouds(self, frame):

        info = frame.getCloudsInformation()
        img = frame.img.copy()
        for cnt in info["contours"]:
            cv2.drawContours(img,[cnt],0,(0,0,255),2)

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, '{} clouds'.format(info["cloudCount"]), (10, 100), font, 1, cv2.LINE_AA)
        cv2.putText(img, '{}% cloudy'.format(round(info["cloudyness"] * 100)), (10, 300), font, 2, cv2.LINE_AA)

        self.imshow(img)