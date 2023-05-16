import cv2


def BGR2YUV(im):
    '''
    input:
        im: BGR
    return:
        YUV
    '''
    yuv = cv2.cvtColor(im, cv2.COLOR_BGR2YUV)
    return yuv


def BGR2HSV(im):
    '''
    input:
        im: BGR
    return:
        HSV
    '''
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    return hsv
