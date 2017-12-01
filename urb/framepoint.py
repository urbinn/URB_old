import sys

from disparity import *
from constants import *
from disparity import *
from imageio import *

class FramePoint:
    def __init__(self, frame, x, y):
        self.id = None
        self.matches = None
        self.cx = x
        self.cy = y
        self.frame = frame
        self.leftx = int(x) - HALF_PATCH_SIZE
        self.topy =int(y) - HALF_PATCH_SIZE  
        self.keypoint = cv2.KeyPoint(x, y, 1, 0)
        self.z = None
        self.disparity = None
    
    def get_patch(self):
        try:
            return self.patch
        except:
            self.patch = get_patch(self.frame.get_smoothed(), self.leftx, self.topy)
            return self.patch
        
    def get_mono_patch(self):
        try:
            return self.monopatch
        except:
            self.monopatch = get_patch(self.frame.get_smoothed(), self.leftx + HALF_PATCH_SIZE - MONO_HALF_PATCH_SIZE, self.topy, MONO_PATCH_SIZE)
            return self.monopatch
        
    def get_patch_distance(self, keypoint):
        return cv2.norm(self.get_patch(), keypoint.get_patch(), NORM)
    
    def get_mono_patch_distance(self, keyPoint):
        return cv2.norm(self.get_mono_patch(), keyPoint.get_mono_patch(), NORM)
    
    def get_patch_distanceM(self, keypoint, x, y):
        patch = get_patch(keypoint.frame.get_smoothed(), keypoint.leftx + x, keypoint.topy + y)
        return cv2.norm(self.get_patch(), patch, NORM)
    
    def get_mono_patch_distance_m(self, keypoint, x, y):
        patch = get_patch(keypoint.frame.get_smoothed(), keypoint.leftx + x  + HALF_PATCH_SIZE - MONO_HALF_PATCH_SIZE, keypoint.topy + y, MONO_PATCH_SIZE)
        return cv2.norm(self.get_mono_patch(), patch, NORM)

    # Estimates the subpixel disparity based on a parabola fitting of the three points around the minimum.
    def subpixel_disparity(self, disparity , coords):
        try:
            subdisparity =  (coords[0] - coords[2]) / (2.0 * (coords[0] + coords[2] - 2.0 * coords[1]))
            return -max(disparity + subdisparity, 0.01)
        except:
            return -disparity - 1
    
    #Compute the distance for a patch in the left hand image by computing the disparity of the patch 
    # in the right hand image. A low confidence (near 1) indicates there is another location where the 
    # patch also fits, and therefore the depth estimate may be wrong. 
    # The bestDistance is returned along with its nearest neighbors to facilitate subpixel disparity estimation.
    def get_disparity(self, frameRight):
        if self.leftx < PATCH_SIZE or self.leftx > self.frame.get_width() - PATCH_SIZE or \
          self.topy < PATCH_SIZE or self.topy > self.frame.get_height() - PATCH_SIZE:
            self.disparity = None
            return None
            #raise ValueError('getDisparity called with patch that is wrong size leftx={} topy={}, patch-size={}'.format(self.leftx, self.topy, PATCH_SIZE))
        best_disparity = 0
        best_distance = sys.maxsize
        distances = []
        for disparity in range(0, self.leftx):
            patchR = frameRight.get_smoothed()[self.topy:self.topy+PATCH_SIZE, self.leftx-disparity:self.leftx+PATCH_SIZE-disparity]
            #print(patchL.shape, patchR.shape,leftxstart,patchSize, disparity)
            distance = cv2.norm(self.get_patch(), patchR, NORM)
            distances.append(distance)
            if distance < best_distance:
                best_distance = distance
                best_disparity = disparity

        # bepaal minimale distance op disparities meer dan 1 pixel van lokale optimum 
        minrest = sys.maxsize
        if best_disparity > 1:
            minrest = min(distances[0:best_disparity-1])
        if best_disparity < self.leftx - HALF_PATCH_SIZE - 2:
            minrest = min([minrest, min(distances[best_disparity+2:])])

        # de disparity schatting is onbetrouwbaar als die dicht bij 1 komt
        # gebruik hier als threshold 1.4 om punten eruit te filteren waarvoor we
        # geen betrouwbare disparity estimates kunnen maken
        self.confidence = minrest / (best_distance + 0.01)

        # Geef de beste disparity op pixel niveau terug, met de twee neighbors om subpixel disparity uit te rekenen
        if best_disparity == 0:
            self.disparity = self.subpixel_disparity(best_disparity, [best_distance, distances[1], distances[2]])
        elif best_disparity == self.leftx -1:
            self.disparity = self.subpixel_disparity(best_disparity, [distances[best_disparity-2], distances[best_disparity-1], best_distance])
        else:
            self.disparity = self.subpixel_disparity(best_disparity, [distances[best_disparity-1], best_distance, distances[best_disparity+1]])
        return self.disparity
                                                    
    def get_depth(self):
        if self.z is None and self.disparity is not None:
            self.z = estimated_distance(self.disparity)
        return self.z
    
    def get_keypoint(self):
        return self.keypoint
    
class FramePointTop(FramePoint):
    def __init__(self, frame, x, y):
        FramePoint.__init__(self, frame, x, y)
        self.topy = self.cy

class FramePointBottom(FramePoint):
    def __init__(self, frame, x, y):
        FramePoint.__init__(self, frame, x, y)
        self.topy = self.cy - PATCH_SIZE
        
class KeyFramePoint(FramePoint):
    def __init__(self, framepoint):
        FramePoint.__init__(self, framepoint.frame, framepoint.cx, framepoint.cy)
        self.id = framepoint.id
        self.leftx = framepoint.leftx
        self.topy = framepoint.topy
        self.keypoint = framepoint.keypoint
        self.z = framepoint.z
        self.disparity = framepoint.disparity
        self.samples = [self]
        
    def addSample(self, framepoint):
        self.samples.append(framepoint)
        
    def getSamples(self):
        return self.samples

