import cv2
import matplotlib.pyplot as plt
import numpy as np

from constants import *

FONT = cv2.FONT_HERSHEY_PLAIN
FONTSIZE = 2

def read_image(filename):
    """reads an image from file. cv reads an image as BGR instead of RGB, so need to swap colors"""
    return cv2.imread(filename, 0)
    
def show2(left, right):
    """shows a left and right stereo image side by side"""
    fig = plt.figure(figsize=(20,6))
    fig.add_subplot(1,2,1)
    plt.imshow(left)
    fig.add_subplot(1,2,2)
    plt.imshow(right)
    plt.show()
    
def show(img):
    """shows a left and right stereo image side by side"""
    plt.figure(figsize=(20,6))
    plt.imshow(img)
   
def draw_frame(frame):
    return draw_framepoints(frame.get_framepoints())

def draw_frame_depth(frame):
    return draw_framepoints_depth(frame.get_framepoints())

def draw_frame_id(frame):
    return draw_framepoints_id(frame.get_framepoints())

def draw_framepoints(framepoints):
    img = framepoints[0].frame.get_image()
    img = cv2.drawKeypoints(img,[kp.get_keypoint() for kp in framepoints],None,color=(0,255,0), flags=0)
    return img

def draw_framepoints_depth(framepoints):
    img = draw_framepoints(framepoints)
    for p in framepoints:
        if p.get_depth() is not None:
            text = '%.1f'%(p.get_depth())
            cv2.putText(img, text, (int(p.cx), int(p.cy)), FONT, FONTSIZE, (255, 0, 0), 1, cv2.LINE_AA)
    return img

def draw_compare_id(frame1, frame2, id):
    p1 = [p for p in frame1.get_framepoints() if p.id == id]
    p2 = [p for p in frame2.get_framepoints() if p.id == id]
    show2(draw_framepoints_depth(p1), draw_framepoints_depth(p2))

def draw_keyframepoints_id(framepoints):
    img = draw_framepoints(framepoints)
    for p in framepoints:
         cv2.putText(img, str(p.id), (int(p.cx), int(p.cy)), FONT, FONTSIZE, (255, 0, 0), 1, cv2.LINE_AA)
    return img

def draw_framepoints_id(framepoints):
    img = draw_framepoints(framepoints)
    for p in framepoints:
        if p.matches is not None:
            cv2.putText(img, str(p.matches.id), (int(p.cx), int(p.cy)), FONT, FONTSIZE, (255, 0, 0), 1, cv2.LINE_AA)
    return img

def get_patch(image, leftx, topy, patch_size = PATCH_SIZE):
    patch = image[topy:topy+patch_size, leftx:leftx+patch_size]
    if patch.shape[0] != patch_size or patch.shape[1] != patch_size:
        raise ValueError('illegal patch size leftx={} topy={} shape={} patch_size={}'.format(leftx, topy, patch.shape, patch_size))
    return patch

ZERO_IMAGE = None
def zero_image(img):
    global ZERO_IMAGE
    if ZERO_IMAGE is None or ZERO_IMAGE.shape != img.shape:
        ZERO_IMAGE = np.zeros(img.shape, np.uint8)
    return ZERO_IMAGE

