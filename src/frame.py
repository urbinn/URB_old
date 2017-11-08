class Frame:
    def __init__(self):
        self.id = 0
        self.points = []

    def extract_orbs(self, left, right, flag):
        if (flag):
            # extract from left image
            kpl, desl = orb.detectAndCompute(left, None)
            # extract from right image
        
        
        self.points.append(point)
