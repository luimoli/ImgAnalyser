import cv2


def splitChannelYUV(im):
    '''
    input:
        im: BGR
    return:
        Y, U, V
    '''
    yuv = cv2.cvtColor(im, cv2.COLOR_BGR2YUV)
    y, u, v = cv2.split(yuv)
    return y, u, v


def splitChannelHSV(im):
    '''
    input:
        im: BGR
    return:
        H, S, V
    '''
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    return h, s, v


def splitChannelBGR(im):
    '''
    input:
        im: BGR
    return:
        B, G, R
    '''
    b, g, r = cv2.split(im)
    return b, g, r


def getY(im):
    '''
    input:
        im: BGR
    return:
        Y_channel
    '''
    y = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    return y
