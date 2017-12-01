import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys
from collections import defaultdict

from filters import *
from framepoint import *
from imageio import *
from constants import *

class Frame:
    def __init__(self, filepath):
        self.filepath = filepath
        self.image = read_image(filepath)

    def read_corresponding(self, path):
        self.right_frame = Frame('/'.join([path, self.filepath.split('/')[-1]]))
        return self.right_frame
        
    def get_image(self):
        return self.image
    
    def get_width(self):
        return self.image.shape[1]
    
    def get_height(self):
        return self.image.shape[0]

    # blur the image to supress noise from being detected
    def get_smoothed(self):
        try:
            return self.smoothed
        except:
            self.smoothed = cv2.GaussianBlur(self.image,(5,5),0)
        return self.smoothed
    
    # compute the median of the single channel pixel intensities for thresholding
    def get_median(self):
        try:
            return self.median
        except:
            self.median = np.median(self.image) * 0.95
        return self.median

    # helper function that filters out overlapping keypoints that are close in depth, thus probably belonging to the same object.
    # Of two overlapping keypoints, the keypoint with the largest confidence is kept.
    def filterNN(self, matched_framepoints):
        # matchedKeyPoints = [(keypoint, x, y, z, confidence)]
        # sort the matchedKeypoints on their estimated depth
        matched_framepoints.sort(key=lambda x: -x.disparity)
        startNN = len(matched_framepoints) - 1
        i = startNN - 1
        remove = []
        while i > 0:
            i -= 1
            for j in range(startNN, i, -1):
                if matched_framepoints[j].get_depth() - matchedKeyPoints[i].get_depth() > 1:
                    startNN = j - 1
                    continue
                if abs(matched_framepoints[j].cx - matched_framepoints[i].cx) < PATCH_SIZE and \
                    abs(matched_framepoints[j].cy - matched_framepoints[i].cy) < PATCH_SIZE:
                    if matched_framepoints[i].confidence < matched_framepoints[j].confidence:
                        del matched_framepoints[i]
                        startNN -= 1
                        if len(remove) > 0:
                            remove = []
                        break
                    else:
                        remove.append(j)
            if len(remove) > 0:
                for j in remove:
                    del matched_framepoints[j]
                startNN -= len(remove)
                remove = []
        return matched_framepoints

    def compute_depth(self):
        # find the disparity for all keypoints between the left and right image
        for kp in self.framepoints:
            kp.get_disparity(self.right_frame)

    def filter_non_stereo(self, confidence=CONFIDENCE):
        self.framepoints = [fp for fp in self.framepoints if fp.disparity is not None and fp.confidence > confidence]

    def filter_non_id(self):
        self.framepoints = [fp for fp in self.framepoints if fp.id is not None]

    def filterNN(self,):
        self.framepoints = self.filterNN(self.framepoints)
        
    def get_framepoints(self):
        try:
            return self.framepoints
        except:
            zeroimage = zero_image(self.get_smoothed())
            #higher_vertical_edges = higher_vertical_edge(self.get_smoothed(), self.get_median())
            higher_vertical_edges = sobelv(self.get_smoothed(), self.get_median() * 1.1)
            #lower_vertical_edges = lower_vertical_edge(self.get_smoothed(), self.get_median())
            lower_vertical_edges = higher_vertical_edges

            veTop = top_vertical_edge(higher_vertical_edges)
            veBottom = bottom_vertical_edge(lower_vertical_edges)
            veTop[0:PATCH_SIZE,:] = zeroimage[0:PATCH_SIZE,:]
            veTop[:,:HALF_PATCH_SIZE] = zeroimage[:,:HALF_PATCH_SIZE]
            veTop[:,-HALF_PATCH_SIZE:] = zeroimage[:,-HALF_PATCH_SIZE:]
            veBottom[-PATCH_SIZE:,:] = zeroimage[-PATCH_SIZE:,:]
            veBottom[:,:HALF_PATCH_SIZE] = zeroimage[:,:HALF_PATCH_SIZE]
            veBottom[:,-HALF_PATCH_SIZE:] = zeroimage[:,-HALF_PATCH_SIZE:]
            
            # combine pixels found at the top and bottom of edges
            # results in an image where keypoints are set as pixels with a 255 intensity
            #keypointImage = veTop + veBottom

            #convert from pixels in an image to KeyPoints
            keypoints = np.column_stack(np.where(veTop >= 255))
            toppoints = [FramePointBottom(self, x, y) for y,x in keypoints]
            keypoints = np.column_stack(np.where(veBottom >= 255))
            bottompoints = [FramePointTop(self, x, y) for y,x in keypoints]
            self.framepoints = toppoints + bottompoints
            for i,f in enumerate(self.framepoints):
                f.id = i
            return self.framepoints

   