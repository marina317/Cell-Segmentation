import numpy as np
import cv2 as cv



def preprocessing(img):
    kernel = np.ones((5, 5))
    blur = cv.blur(img, kernel, 0)
    _,binary = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
    binary = binary.astype(np.uint8)
    closed = cv.morphologyEx(binary, cv.MORPH_CLOSE,kernel)
    opened = cv.morphologyEx(closed, cv.MORPH_OPEN, kernel)
    return opened

def watershed(img, preprocessed_img):
    kernel = np.ones((5, 5))
    sure_bg = cv.dilate(preprocessed_img,kernel,iterations=3) 
    kernel = np.ones((3,3))
    sure_fg = cv.erode(preprocessedImg, kernel,iterations = 3)
    unknown = cv.subtract(sure_bg,sure_fg)

    ret, markers = cv.connectedComponents(sure_fg)
    markers = markers+1
    markers[unknown==255] = 0
    img = img.astype(np.uint8)
    img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)

    markers = markers.astype(np.int32)
    markers = cv.watershed(img, markers)
    return img


def run_pipeline(img, i):
    preprocessed = preprocessing(img)
    result = watershed(img, preprocessed)
    return result
