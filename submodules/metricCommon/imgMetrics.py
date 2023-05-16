import numpy as np
import cv2
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim


def calcPSNR(imtest, imref=None):
    '''
    input:
        imtest: [H, W, C]
        imref: [H, W, C]
    return:
        psnr: dB
    '''
    if imref is None:
        imref = imtest
        imref = cv2.GaussianBlur(imref, (5, 5), 3)
    res = psnr(imref, imtest)
    return round(res, 5)


def calcSSIM(imtest, imref=None):
    '''
    input:
        imtest: [H, W, C]
        imref: [H, W, C]
    return:
        ssim
    '''
    if imref is None:
        imref = imtest
        imref = cv2.GaussianBlur(imref, (5, 5), 3)

    if len(imtest.shape) == 3:
        res = ssim(imref, imtest, channel_axis=2, multichannel=True)
    else:
        res = ssim(imref, imtest)
    return round(res, 5)


def calcSNR(imtest):
    '''
    input:
        imtest: [H, W, 1]   single channel image
    return:
        snr: dB
    '''
    imsignal = cv2.GaussianBlur(imtest, (5, 5), 1)
    imnoise = imtest - imsignal
    snr = 20*np.log10(imsignal.mean()/imnoise.mean())
    return snr
