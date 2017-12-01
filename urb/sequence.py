import sys
import os
import shutil

def save_keyframepoints(filename, keyFramePoints):
    with open(filename, 'w') as fout:
        for p in keyFramePoints:
            fout.write('%d %d %d %f\n'%(p.id, p.cx, p.cy, p.get_depth()))

def save_framepoints(filename, frame_points):
    with open(filename, 'w') as fout:
        for p in frame_points:
            if p.matches is not None and p.matches.get_depth() is not None:
                fout.write('%d %d %d %f %d %d\n'%(p.matches.id, p.matches.cx, p.matches.cy, p.matches.get_depth(), p.cx, p.cy))

# returns the two best matching points in the list of keyPoints for the given query keyPoint
def matching_framepoint(frame_point, frame_points):
    if len(frame_points) < 2:
         return (0, None)
    best_distance = sys.maxsize
    next_best_distance = sys.maxsize
    best_frame_point = None
    for kp in frame_points:
        distance = kp.get_patch_distance(frame_point)
        if distance < best_distance:
            next_best_distance = best_distance
            best_distance = distance
            best_frame_point = kp
        elif distance < next_best_distance:
            next_best_distance = distance
    confidence = next_best_distance / (best_distance + 0.01)
    return (confidence, best_frame_point)

# returns the matching keyPoints in a new frame to keyPoints in a keyFrame that exceed a confidence score
def match_frame(frame, frame_points, confidence_threshold = 1.4):
    for kp in frame_points:
        confidence, fp = matching_framepoint(kp, frame.get_framepoints())
        if confidence > confidence_threshold and fp.matches is None:
            fp.matches = kp
            
def track(folder, frames):
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.mkdir(folder)
    save_framepoints(folder + '/0.txt', frames[0].get_framepoints())
    id = 0
    for i in range(len(frames)):
        for f in frames[i].get_framepoints():
            f.id = id
            id += 1

    for j in range(1, len(frames)):
        for i in range (max(0, j - 6), j):
            for p in frames[j].get_framepoints():
                p.matches = None
            match_frame(frames[j], frames[i].get_framepoints(), confidence_threshold = 1.4)
            save_framepoints(folder + '/' + str(i) + '-' + str(j) + '.txt', frames[j].get_framepoints())

def create_sequence(frames):
    s = Sequence(frames[0])
    for i in range(1, len(frames)):
        s.add_frame(frames[i]);
    return s

class Sequence:
    def __init__(self, keyframe):
        keyframe.compute_depth()
        keyframe.filter_non_stereo()
        self.keyframe = keyframe
        self.keyframepoints = keyframe.get_framepoints()
        for i, fp in enumerate(self.keyframepoints):
            fp.id = i
        self.other_frames = []

    def add_frame(self, frame, confidence_threshold = 1.4):
        frame.compute_depth()
        frame.filter_non_stereo()
        match_frame(frame, self.keyframepoints, confidence_threshold = confidence_threshold)
        self.other_frames.append(frame)
                
    def dump(self, folder):
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.mkdir(folder)
        save_keyframepoints(folder + '/0.txt', self.keyframepoints)
        for i, frame in enumerate(self.other_frames):
            save_framepoints(folder + '/' + str(i+1) + '.txt', frame.get_framepoints())
                
    def counts(self):
        r = [0] * len(self.keyframepoints)
        for f in self.other_frames:
            for p in f.get_framepoints():
                r[p.id] += 1
        return r