import numpy as np
import cv2 as cv

def preprocessing(img):
    # 1. cv.blur expects a tuple (5, 5) for ksize
    blur = cv.blur(img, (5, 5))

    # 2. Thresholding
    _, binary = cv.threshold(blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    binary = binary.astype(np.uint8)

    # 3. Morphological operations (these use numpy matrix kernels)
    kernel_matrix = np.ones((5, 5), np.uint8)
    closed = cv.morphologyEx(binary, cv.MORPH_CLOSE, kernel_matrix)
    opened = cv.morphologyEx(closed, cv.MORPH_OPEN, kernel_matrix)

    # 4. MUST return the result!
    return opened


def watershed(img, preprocessed_img):
    kernel = np.ones((3, 3), np.uint8)

    # Background and Foreground area calculation
    sure_bg = cv.dilate(preprocessed_img, kernel, iterations=3) 
    sure_fg = cv.erode(preprocessed_img, kernel, iterations=3)
    unknown = cv.subtract(sure_bg, sure_fg)

    # Marker labelling
    ret, markers = cv.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0

    # cv.watershed requires a 3-channel 8-bit BGR image
    if len(img.shape) == 2:
        img_color = cv.cvtColor(img.astype(np.uint8), cv.COLOR_GRAY2BGR)
    else:
        img_color = img.astype(np.uint8)

    markers = markers.astype(np.int32)
    cv.watershed(img_color, markers)

    # Boundary line is marked with -1
    img_color[markers == -1] = [0, 0, 255]  # Red boundary lines
    return img_color


def run_pipeline(img):
    preprocessed = preprocessing(img)
    result = watershed(img, preprocessed)
    return result
