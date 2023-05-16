import numpy as np


def getDis(im, p1: list, p2: list, channel=None):
    '''
    input:
        im: [H, W, C] C==1 or C==3
        p1: point idx <list>
        p2: point idx <list>
        channel: <int> the idx of channel [0, 1, 2]
    return:
        coorDis: <int>
        colorDis: <int>
    '''
    assert len(im.shape) == 2 or len(im.shape) == 3, 'error'
    p1 = np.array(p1)
    p2 = np.array(p2)
    p1 = p1[..., ::-1]
    p2 = p2[..., ::-1]
    coorDis = p1 - p2
    im = np.float32(im)
    if len(im.shape) == 3:
        if channel is None:
            colorDis = im[p1[0], p1[1], :] - im[p2[0], p2[1], :]
            # print(im[p1[0], p1[1], :])
            # print(im[p2[0], p2[1], :])
            # print(colorDis)
        else:
            colorDis = im[p1[0], p1[1], channel] - im[p2[0], p2[1], channel]
    else:
        colorDis = im[p1[0], p1[1]] - im[p2[0], p2[1]]

    coorDis = np.sqrt(np.sum(np.power(coorDis, 2)))
    colorDis = np.sqrt(np.sum(np.power(colorDis, 2)))

    return coorDis, colorDis
