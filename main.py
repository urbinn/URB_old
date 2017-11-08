import cv2

from lib.frame import Frame
from lib.point import Point
from lib.system import System

if __name__ == '__main__':
    ORB_CONFIG = {
        "edgeThreshold": 1,
        "patchSize": 15,
        "nlevels": 1,
        "fastThreshold": 1,
        "scaleFactor": 1.2,
        "WTA_K": 2,
        "scoreType": cv2.ORB_HARRIS_SCORE,
        "firstLevel": 0,
        "nfeatures": 2000
    }

    system = System(ORB_CONFIG)

