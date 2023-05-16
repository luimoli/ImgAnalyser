import cv2
import numpy as np


from PyQt5 import QtCore 
from PyQt5.QtGui import QImage, QPixmap

from submodules.metricCommon.imgMetrics import calcPSNR, calcSSIM, calcSNR
from submodules.imgCommon.imgChannel import getY
from submodules.imgCommon.imgOperator import diffImgs

from utils.plt2cvimg import plotHeatmap

class Handler_mm(object):
    def __init__(self,  ui) -> None:
        self.ui = ui
        self.ratio_value = 100
    
    def set_img_path(self, path_list):
        self.img1_path, self.img2_path = path_list
        self.read_init()
    
    def read_init(self):
        try:
            self.img1 = cv2.imread(self.img1_path)
            self.img1_height, self.img1_width, self.img1_channel = self.img1.shape            
        except:
            self.img1 = cv2.imread('./img/default.jpg')
            self.img1_height, self.img1_width, self.img1_channel = self.img1.shape

        self.img1_rgb = self.img1[:,:,::-1].copy()
        self.img1_qpixmap = self.__transform_cvimg_to_pixmap(self.img1)


        try:
            self.img2 = cv2.imread(self.img2_path)
            self.img2_height, self.img2_width, self.img2_channel = self.img2.shape            
        except:
            self.img2 = cv2.imread('./img/default.jpg')
            self.img2_height, self.img2_width, self.img2_channel = self.img2.shape

        self.img2_rgb = self.img2[:,:,::-1].copy()
        self.img2_qpixmap = self.__transform_cvimg_to_pixmap(self.img2)


        self.ratio_value = 100
        self.set_img_ratio()
        # self.__update_text_file_path()
    
    def set_img_ratio(self):
        # self.ratio_rate = pow(10, (self.ratio_value - 50)/50)
        self.ratio_rate = self.ratio_value / 100
        qpixmap_height = int(self.img1_height * self.ratio_rate)
        qpixmap_width = int(self.img1_width * self.ratio_rate)
        self.img1_resize = cv2.resize(self.img1, (qpixmap_width, qpixmap_height), interpolation=cv2.INTER_CUBIC)
        self.img1_qpixmap = self.__transform_cvimg_to_pixmap(self.img1_resize)

        qpixmap_height = int(self.img2_height * self.ratio_rate)
        qpixmap_width = int(self.img2_width * self.ratio_rate)
        self.img2_resize = cv2.resize(self.img2, (qpixmap_width, qpixmap_height), interpolation=cv2.INTER_CUBIC)
        self.img2_qpixmap = self.__transform_cvimg_to_pixmap(self.img2_resize)
        self.__update_img()
        self.__update_text_ratio()

    def get_wheel_value(self, event):
        if self.img1 is not None and self.img2 is not None:
            angle = event.angleDelta() / 8
            angleY = angle.y()
            if angleY > 0:
                self.ratio_value += 5
                self.ratio_value = min(500, self.ratio_value)
            else: 
                self.ratio_value -= 5
                self.ratio_value = max(10, self.ratio_value)
            self.set_img_ratio()
    
    def calc_metric(self, metricname):
        if self.img1 is not None and self.img2 is not None:
            if metricname == 'PSNR':
                value = calcPSNR(self.img1, self.img2)  
            elif metricname == 'SSIM':
                value = calcSSIM(self.img1, self.img2)
            self.ui.lineEdit.setText(f'{value:.2f}')
    
    def get_diff_map(self, channelname):
        if self.img1 is not None and self.img2 is not None:
            img1_b, img1_g, img1_r = cv2.split(self.img1)
            img2_b, img2_g, img2_r = cv2.split(self.img2)
            if channelname == 'R':
                diffimg = diffImgs(img1_r, img2_r)
            elif channelname == 'B':
                diffimg = diffImgs(img1_b, img2_b)
            elif channelname == 'G':
                diffimg = diffImgs(img1_g, img2_g)
            elif channelname == 'Y':
                img1_Y = getY(self.img1)
                img2_Y = getY(self.img2)
                diffimg = diffImgs(img1_Y, img2_Y)
            heatmap = plotHeatmap(diffimg)
            pixmap = self.__transform_cvimg_to_pixmap(heatmap)
            return pixmap


    
    def __update_img(self):
        self.ui.label_img1.setPixmap(self.img1_qpixmap)
        self.ui.label_img1.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.ui.label_img2.setPixmap(self.img2_qpixmap)
        self.ui.label_img2.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
    
    def __update_text_ratio(self):
        self.ui.label_ratio1.setText(f'{round(100*self.ratio_rate)}%')
        self.ui.label_ratio2.setText(f'{round(100*self.ratio_rate)}%')\

    def __transform_cvimg_to_pixmap(self, cvimg):
        """
        Args: cvimg (opencv img arr): B-G-R format
        """
        height, width = cvimg.shape[:2]
        if len(cvimg.shape) == 2:
            cvimg = np.expand_dims(cvimg,-1).repeat(3,axis=-1)
        qimg = QImage(cvimg, width, height,  width * 3, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(qimg)
        return pixmap