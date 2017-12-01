# TODO: Uitlezen van calibratie file
bf = 386.1448 

def estimated_distance(disparity):
    return -bf / disparity

def patch_disparity(framepoint, frame_right):
    frame_left = framepoint.frame
    if framepoint.cy < PATCH_SIZE or framepoint.cy > frame_left.getHeight() - PATCH_SIZE or \
        framepoint.cx < PATCH_SIZE or framepoint.cx > frame_left.getWidth() - PATCH_SIZE:
            return None
    startx = framepoint.startx
    best_disparity = 0
    best_distance = sys.maxsize
    distances = []
    for disparity in range(0, startx):

        patchL = framepoint.get_patch()
        patchR = frame_right.get_image()[starty:starty+PATCH_SIZE, startx-disparity:startx+PATCH_SIZE-disparity]
        #print(patchL.shape, patchR.shape,leftxstart,patchSize, disparity)
        distance = cv2.norm(patchL, patchR, NORM)
        distances.append(distance)
        if distance < best_distance:
            best_distance = distance
            best_disparity = disparity
    
    # bepaal minimale distance op disparities meer dan 1 pixel van lokale optimum 
    minrest = sys.maxsize
    if best_disparity > 1:
        minrest = min(distances[0:best_disparity-1])
    if best_disparity < startx - HALF_PATCH_SIZE - 2:
        minrest = min([minrest, min(distances[best_disparity+2:])])
        
    # de disparity schatting is onbetrouwbaar als die dicht bij 1 komt
    # gebruik hier als threshold 1.4 om punten eruit te filteren waarvoor we
    # geen betrouwbare disparity estimates kunnen maken
    confidence = minrest / best_distance
    
    # Geef de beste disparity op pixel niveau terug, met de twee neighbors om subpixel disparity uit te rekenen
    if best_disparity == 0:
            return (best_disparity, [best_distance, distances[1], distances[2]], confidence)
    elif best_disparity == startx -1:
        return (best_disparity, [distances[best_disparity-2], distances[best_disparity-1], best_distance], confidence)
    return (best_disparity, [distances[best_disparity-1], best_distance, distances[best_disparity+1]], confidence)