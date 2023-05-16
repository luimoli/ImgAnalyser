import cv2
import numpy as np


def calcHist(src, bins=256):
    '''
    input:
        src:
            img: [H, W, 1] single channel image
            line: [L, 1] single channel Line
        bins:
            the number of bin.
    return:
        histogram
    '''
    src = np.array(src)
    assert len(src.shape) == 2 or len(src.shape) == 1, 'ERROR'
    hist = cv2.calcHist([src], [0], None, [bins], [0, bins])
    return hist
