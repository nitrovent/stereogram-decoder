import cv2
import numpy as np

def decode_stereogram(img):
    depthmap = depth_map(img, img)
    inverted = 255-depthmap
    normalized = cv2.normalize(inverted, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    return normalized

def depth_map(imgL, imgR):

    window_size = 5 
    numDisparities = 16*imgL.shape[1]//90

    left_matcher = cv2.StereoSGBM_create(
        minDisparity=3,
        numDisparities=numDisparities,
        blockSize=window_size,
        P1=9 * 3 * window_size,
        P2=128 * 3 * window_size,
        disp12MaxDiff=12,
        uniquenessRatio=10,
        speckleWindowSize=50,
        speckleRange=32,
        preFilterCap=63,
        mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY
    )
    
    right_matcher = cv2.ximgproc.createRightMatcher(left_matcher)

    lmbda = 50000
    sigma = 2.7

    wls_filter = cv2.ximgproc.createDisparityWLSFilter(matcher_left=left_matcher)
    wls_filter.setLambda(lmbda)
    wls_filter.setSigmaColor(sigma)

    displ = left_matcher.compute(imgL, imgR) 
    dispr = right_matcher.compute(imgR, imgL) 

    filteredImg = wls_filter.filter(displ, imgL, None, dispr) 
    filteredImg = cv2.normalize(src=filteredImg, dst=filteredImg, beta=0, alpha=255, norm_type=cv2.NORM_MINMAX);
    filteredImg = np.uint8(filteredImg)

    croppedImg = filteredImg[0:filteredImg.shape[0], numDisparities+window_size:filteredImg.shape[1]]

    return croppedImg