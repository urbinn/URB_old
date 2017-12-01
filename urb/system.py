import cv2
import matplotlib.pyplot as plt

class System:
    def __init__(self, config, calibration):
        self.frames = []
        self.orb_params = cv2.ORB_create(
            edgeThreshold = config["edgeThreshold"],
            patchSize = config["patchSize"],
            nlevels = config["nlevels"],
            fastThreshold = config["fastThreshold"],
            scaleFactor = config["scaleFactor"],
            WTA_K = config["WTA_K"],
            scoreType = config["scoreType"],
            firstLevel = config["firstLevel"],
            nfeatures = config["nfeatures"]
        )

        self.fx = calibration["fx"]
        self.fy = calibration["fy"]
        self.cx = calibration["cx"]
        self.cy = calibration["cy"]
