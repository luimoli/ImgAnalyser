import copy
import cv2
import numpy as np


def performROI(im, roi: list):
    '''
    input:
        im: [H, W, C] C = 1 or 3
        roi: [p_leftup, p_rightdown]
    return:
        roied_img
    '''
    p_leftup = roi[0]
    p_rightdown = roi[1]
    if len(im.shape) == 2:
        imROI = im[p_leftup[0]: p_rightdown[0], p_leftup[1]: p_rightdown[1]]
    if len(im.shape) == 3:
        imROI = im[p_leftup[0]: p_rightdown[0], p_leftup[1]: p_rightdown[1], :]
    return imROI


def performMask(im, mask):
    '''
    input:
        im: [H, W, C] C = 1 or 3
        mask: [H, W, C] C = 1 or 3
    return:
        maskedImg
    '''
    assert im.shape[:2] == mask.shape[:2], \
        'The shapes of im and mask are different'

    maskedImg = copy.deepcopy(im)
    if len(im.shape) == len(mask.shape):
        assert im.shape == mask.shape, \
            'The shapes of im and mask are different'
        maskedImg[mask == 0] = 0
    if len(im.shape) == 3 and len(mask.shape) == 2:
        maskedImg[mask == 0, :] = 0
    return maskedImg


def getLine(im, p1: list, p2=None):
    '''
    input:
        im: [H, W, C] multichannel or single channel
        p1: point idx
        p2: point idx
    return:
        line:
            if p1 and p2: return np.float32
            only p1: dtype is same with im
    '''
    assert len(im.shape) == 2 or len(
        im.shape) == 3, f'The im should be 2D or 3D, but get {len(im.shape)}D'
    assert p1 is not None, 'ERROR'
    if p2 is None:
        idy, idx = p1[0], p1[1]
        if len(im.shape) == 3:
            HorizontalLine = im[idy, ::]
            VerticalLine = im[:, idx, ::]
        else:
            HorizontalLine = im[idy, :]
            VerticalLine = im[:, idx]
        return HorizontalLine, VerticalLine
    else:
        # y1, y2 = p1[0], p2[0]
        # x1, x2 = p1[1], p2[1]
        x1, x2 = p1[0], p2[0]
        y1, y2 = p1[1], p2[1]
        ll = int(np.floor(np.sqrt(np.power((x1-x2), 2) + np.power(y1-y2, 2))))
        if len(im.shape) == 3:
            Line = np.zeros((ll, 3))
        else:
            Line = np.zeros(ll)
        dy = (y2-y1)/ll
        dx = (x2-x1)/ll
        for i in range(ll):
            cur_y = y1 + i*dy
            cur_x = x1 + i*dx

            up_y = int(np.floor(cur_y))
            down_y = up_y + 1

            left_x = int(np.floor(cur_x))
            right_x = left_x + 1

            # bilinear
            interPxDown = (cur_x - left_x)*im[down_y, left_x] + \
                (right_x - cur_x)*im[down_y, right_x]
            interPxUp = (cur_x-left_x) * im[up_y, left_x] + \
                (right_x - cur_x)*im[up_y, right_x]
            interP = (down_y - cur_y)*interPxDown + (cur_y - up_y)*interPxUp
            Line[i] = interP
        return np.float32(Line)


def diffImgs(im1, im2):
    assert im1.shape == im2.shape, 'The shape of im1 and im2 should be same!'
    return np.abs(im1 - im2)


def test():
    im = cv2.imread('./data/lena.png', cv2.IMREAD_UNCHANGED)[:, :, 1]
    print(getLine(im, [100, 100], [150, 150]).shape)


if __name__ == "__main__":
    test()
