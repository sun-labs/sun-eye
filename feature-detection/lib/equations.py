import math
# implement trigonometric formulas

def dewPoint(relhumid, airtemp):
    return airtemp - ((100 - relhumid)/5)

def cloudHeight(relhumid, airtemp):
    return (relhumid - dewPoint(relhumid, airtemp))/0.00802

def viewportWidth(cloudAltitude, focalAngle):
    rad = math.radians(focalAngle)
    return (cloudAltitude * math.tan(rad))/2