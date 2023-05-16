import cv2
import numpy as np


def getGrad(im, k=3):
    '''
    input:
        im: [H, W, 1] single channel img
        k: kernel size of Sobel, default=3
    return:
        Grad, GradX, GradY
    '''
    GradX = cv2.Sobel(im, -1, 1, 0, ksize=k)
    GradY = cv2.Sobel(im, -1, 0, 1, ksize=k)
    # Grad = np.sqrt(GradX**2 + GradY**2)
    
    # Grad = np.uint8(np.sqrt(np.float32(GradX)**2 + np.float32(GradY)**2))
    Grad = np.uint8(GradX * 0.5 + GradY * 0.5)
    
    return Grad, GradX, GradY


def getFFT(im):
    '''
    input:
        im: [H, W, 1] single channel img
    return:
        fft
    '''
    Freq = np.fft.fft2(np.fft.fftshift(im))
    return Freq
