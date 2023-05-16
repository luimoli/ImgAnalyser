import cv2
import os
import numpy as np

from PyQt5 import QtCore 
from PyQt5.QtGui import QImage, QPixmap

from utils.opencv_engine import opencv_engine
from utils.plt2cvimg import plt2cvimg, plt2cvimg_multisubplots, pltimshow2cvimg
from utils.process import noramlization
from smv_colour import RGB2Lab

from submodules.colorCommon.imgColorTrans import BGR2HSV, BGR2YUV
from submodules.imgCommon.imgChannel import getY
from submodules.imgCommon.imgDistance import getDis
from submodules.analysisCommon.imgAnalysis import calcHist
from submodules.imgCommon.imgOperator import getLine
from submodules.imgCommon.imgTrans import getFFT, getGrad


class Handler_sm(object):
    def __init__(self, ui, ui2) -> None:
        self.ui = ui
        self.ui2 = ui2
        self.ratio_value = 50
        self.img = None
        
        self.mouse_in = False

        self.mode_ROI = False
        self.mode_line = False

        self.index_line_real = []
        self.index_line_click = []
        self.index_ROI_real = [0,0,0,0]
        self.index_ROI_click = [0,0,0,0]
        self.pos_current_real = None
        self.pos_current_cursor = None
        self.index_neib = []

    
    def set_img_path(self, path):
        self.img_path = path
        self.read_init()
        
    def read_init(self):
        try:
            self.img = cv2.imread(self.img_path)
            self.origin_height, self.origin_width, self.origin_channel = self.img.shape            
        except:
            self.img = cv2.imread('./img/default.jpg')
            self.origin_height, self.origin_width, self.origin_channel = self.img.shape

        self.img_rgb = self.img[:,:,::-1].copy()
        self.qimg = QImage(self.img, self.origin_width, self.origin_height,  self.origin_width * 3, QImage.Format_RGB888).rgbSwapped()
        self.original_pixmap = QPixmap.fromImage(self.qimg)
        self.ratio_value = 50
        self.set_img_ratio()
        self.__update_text_file_path()
    
    def set_img_ratio(self):
        self.ratio_rate = pow(10, (self.ratio_value - 50)/50)
        qpixmap_height = int(self.origin_height * self.ratio_rate)
        qpixmap_width = int(self.origin_width * self.ratio_rate)
        ccb_index = self.ui.cbb_resize.currentIndex()
        if ccb_index == 0:
            self.img_resize = cv2.resize(self.img, (qpixmap_width, qpixmap_height), interpolation=cv2.INTER_CUBIC)
        elif ccb_index == 1:
            self.img_resize = cv2.resize(self.img, (qpixmap_width, qpixmap_height), interpolation=cv2.INTER_NEAREST)
        elif ccb_index == 2:
            self.img_resize = cv2.resize(self.img, (qpixmap_width, qpixmap_height), interpolation=cv2.INTER_NEAREST)
        else:
            print('comboBox_resize error!')
        self.qpixmap = self.__transform_cvimg_to_pixmap(self.img_resize)

        # ---- original resize-------
        # self.ratio_rate = pow(10, (self.ratio_value - 50)/50)
        # qpixmap_height = self.origin_height * self.ratio_rate
        # self.qpixmap = self.original_pixmap.scaledToHeight(qpixmap_height)
        #--------------------------
        self.__update_img()
        self.__update_text_ratio()
        self.__update_text_img_shape()

    # def set_zoom_in(self):
    #     self.ratio_value = max(0, self.ratio_value - 1)
    #     self.set_img_ratio()
    
    # def set_zoom_out(self):
    #     self.ratio_value = min(100, self.ratio_value + 1)
    #     self.set_img_ratio()

    # def set_slider_value(self, value):
    #     self.ratio_value = value
    #     self.set_img_ratio()

    # def get_slider_value(self):
    #     self.set_slider_value(self.ui.slider_zoom.value())
    

    def get_wheel_value(self, event):
        if self.img is not None:
            angle = event.angleDelta() / 8  # 返回QPoint对象，为滚轮转过的数值，单位为1/8度
            angleY = angle.y()
            if angleY > 0:
                self.ratio_value += 1
                self.ratio_value = min(100, self.ratio_value)
            else: 
                self.ratio_value -= 1
                self.ratio_value = max(0, self.ratio_value)
            self.set_img_ratio()
    
    
    
    #-----------neighbor------------------------
    def show_neib_value(self):
        if self.pos_current_real and self.img is not None:
            radius = self.ui.spinBox_range.value()
            x, y = self.pos_current_real
            upleft_x, upleft_y = max(0, x-radius), max(0, y-radius)
            dnright_x, dnright_y = min(self.origin_width-1, x+radius), min(self.origin_height-1, y+radius) # TODO:border range?
            self.index_neib = [upleft_x, upleft_y, dnright_x, dnright_y]
            img_neib = self.__get_img_by_index(self.img, self.index_neib)
            img_Y_neib = getY(img_neib)
            avg_Y = np.mean(img_Y_neib)
            avg_std = np.std(img_neib, axis=(0, 1))
            self.ui.lineEdit_neib_avg_Y.setText(f'{avg_Y:.2f}')
            self.ui.lineEdit_neib_sd.setText(f'{avg_std[2]:.2f}, {avg_std[1]:.2f}, {avg_std[0]:.2f}')
            pixmap = self.__get_ROI_his_RGBY(self.img, self.index_neib)
            self.ui2.label_map.setPixmap(pixmap)
            self.ui2.label_map.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)


    def clear_neib_value(self):
        self.ui.lineEdit_neib_avg_Y.setText('')
        self.ui.lineEdit_neib_sd.setText('')
    

    def __get_his(self, img):
        his = calcHist(img)
        his_cvimg = plt2cvimg(his)
        his_qpixmap = self.__transform_cvimg_to_pixmap(his_cvimg)
        return his_qpixmap
        

    def get_move_position(self, event):
        if self.img is not None:
            x = event.pos().x()
            y = event.pos().y()
            real_pos_x, real_pos_y = self.__transform_eventpos_to_realpos(x, y)
            self.pos_current_cursor = (x, y)
            self.pos_current_real = (real_pos_x, real_pos_y) 
            self.show_cursor_RGB()
            if self.ui.cbb_neib_show.currentIndex():
                self.show_neib_value()

    def show_cursor_RGB(self):
        real_pos_x, real_pos_y = self.pos_current_real
        if real_pos_x < self.origin_width and real_pos_y < self.origin_height:
            current_RGB = self.img_rgb[real_pos_y][real_pos_x]
            self.ui.label_real_pos.setText(f"| X = {real_pos_x}, Y = {real_pos_y} |")
            self.ui.label_rgb.setText(f"RGB = ({current_RGB[0]}, {current_RGB[1]}, {current_RGB[2]})")
        else:
            self.pos_current_cursor, self.pos_current_real = None, None
            self.ui.label_real_pos.setText(f"")
            self.ui.label_rgb.setText(f"")
            if self.ui.cbb_neib_show.currentIndex():
                self.clear_neib_value()
    
    def stop_cursor_RGB(self):
        self.pos_current_cursor, self.pos_current_real = None, None
        self.ui.label_real_pos.setText(f"")
        self.ui.label_rgb.setText(f"")
        if self.ui.cbb_neib_show.currentIndex():
                self.clear_neib_value()

    # def get_line_clicked_position(self, event):
    #     if self.img is not None and self.mode_line:
    #         if len(self.index_line_real) == 2:
    #             self.index_line_real = []
    #             self.index_line_click = []
    #         x = event.pos().x()
    #         y = event.pos().y()
    #         real_pos_x, real_pos_y = self.__transform_eventpos_to_realpos(x, y)
            
    #         if len(self.index_line_real) < 2:
    #             self.index_line_real.append((real_pos_x, real_pos_y))
    #             self.index_line_click.append((x, y))
    #         if len(self.index_line_real) == 2:
    #             self.create_line_img()


    def calc_line_distance(self, index):
        if self.mode_line and self.index_line_real:
            start_pos = self.index_line_real[0]
            end_pos = self.index_line_real[1]

            if index == 0:
                dis = pow((pow((start_pos[0]-end_pos[0]), 2) + pow((start_pos[1] - end_pos[1]), 2)), 1/2)
            elif index == 1:
                _, dis = getDis(self.img, start_pos, end_pos)
            elif index == 2:
                yuv_img = BGR2YUV(self.img)
                _, dis = getDis(yuv_img, start_pos, end_pos)
            elif index == 3:
                lab_img = RGB2Lab(self.img_rgb, 'bt709')
                _, dis = getDis(lab_img, start_pos, end_pos)
            self.ui.lineEdit_distance.setText(f'{dis:.2f}')
                

    def create_line_img(self):
        if self.mode_line:
            img_resize = self.img_resize.copy()
            start_point, end_point = self.index_line_click
            img_line = opencv_engine.draw_line(img_resize, start_point, end_point) 
            self.qpixmap = self.__transform_cvimg_to_pixmap(img_line)
            self.__update_img()
            self.calc_line_distance(0)

    def clear_line_img(self):
        self.qpixmap = self.__transform_cvimg_to_pixmap(self.img_resize)
        self.__update_img()
        self.index_line_real = []
        self.index_line_click = []


    def get_clicked_position(self, event):
        if self.img is not None:
            x = event.pos().x()
            y = event.pos().y()
            real_pos_x, real_pos_y = self.__transform_eventpos_to_realpos(x, y)
            if self.mode_line:
                if len(self.index_line_real) == 2:
                    self.index_line_real = []
                    self.index_line_click = []

                if len(self.index_line_real) < 2:
                    self.index_line_real.append((real_pos_x, real_pos_y))
                    self.index_line_click.append((x, y))

                if len(self.index_line_real) == 2:
                    self.create_line_img()

            if self.mode_ROI:
                self.index_ROI_real[0:2] = real_pos_x, real_pos_y
                self.index_ROI_click[0:2] = x, y


    def get_ROI_finished_position(self, event):
        if self.img is not None and self.mode_ROI:
            x = event.pos().x()
            y = event.pos().y()
            real_pos_x, real_pos_y = self.__transform_eventpos_to_realpos(x, y)
            self.index_ROI_real[2:] = real_pos_x, real_pos_y
            self.index_ROI_click[2:] = x, y
            self.create_ROI_img()

    def create_ROI_img(self):
        if self.mode_ROI:
            img_resize = self.img_resize.copy()
            img_ROI = opencv_engine.draw_rectangle_by_points(img_resize, self.index_ROI_click[0:2], self.index_ROI_click[2:]) 
            self.qpixmap = self.__transform_cvimg_to_pixmap(img_ROI)
            self.__update_img()
            self.calc_ROI_metric()


    def clear_ROI_img(self):
        self.qpixmap = self.__transform_cvimg_to_pixmap(self.img_resize)
        self.__update_img()
        self.clear_ROI_metric()
        self.index_ROI_click = [0,0,0,0]
        self.index_ROI_real = [0,0,0,0]


    def calc_ROI_metric(self):
        img_roi = self.__get_img_by_index(self.img, self.index_ROI_real)
        img_Y_roi = getY(img_roi)
        avg_bgr = np.mean(img_roi, axis=(0, 1))
        avg_y = np.mean(img_Y_roi)
        avg_std = np.std(img_roi, axis=(0, 1))
        self.ui.lineEdit_ROI_avg_RGB.setText(f'{avg_bgr[2]:.2f}, {avg_bgr[1]:.2f}, {avg_bgr[0]:.2f}') # bgr -> rgb
        self.ui.lineEdit_ROI_avg_Y.setText(f'{avg_y:.2f}')
        self.ui.lineEdit_ROI_sd.setText(f'{avg_std[2]:.2f}, {avg_std[1]:.2f}, {avg_std[0]:.2f}') 
    
    def clear_ROI_metric(self):
        self.ui.lineEdit_ROI_avg_RGB.setText('')
        self.ui.lineEdit_ROI_avg_Y.setText('')
        self.ui.lineEdit_ROI_sd.setText('')


    # ----------histogram----------------------
    def get_global_his(self):
        if self.img is not None:
            img_Y = getY(self.img_rgb)
            global_his = []
            titile_list = ['R','G','B','Y']
            for i in range(self.origin_channel):
                global_his.append(calcHist(self.img_rgb[:,:,i].copy()))
            global_his.append(calcHist(img_Y))
            global_his_cvimg = plt2cvimg_multisubplots(global_his, titile_list)
            global_his_qpixmap = self.__transform_cvimg_to_pixmap(global_his_cvimg)
            return global_his_qpixmap

    def get_ROI_his(self):
        if self.img is not None and any(self.index_ROI_real):
            return self.__get_ROI_his_RGBY(self.img, self.index_ROI_real)


    def get_Line(self):
        p1, p2 = self.index_line_real
        img_line = getLine(self.img, p1, p2)
        return img_line
    
    def get_Line_his(self):
        if self.img is not None and len(self.index_line_real):
            img_line = self.get_Line()
            his_line = calcHist(img_line)
            his_cvimg = plt2cvimg(his_line)
            his_qpixmap = self.__transform_cvimg_to_pixmap(his_cvimg)
            return his_qpixmap

    def get_Line_plot(self):
        if self.img is not None and len(self.index_line_real):
            img_line = self.get_Line()
            plot_cvimg = plt2cvimg(img_line)
            plot_qpixmap = self.__transform_cvimg_to_pixmap(plot_cvimg)
            return plot_qpixmap
    

    def get_gradient_map(self, flag, channel):
        """_summary_
        Args:
            flag (int): [0,1,2] for Grad, GradX, GradY
            channel (str): ['R','G','B','Y']
        Returns:
            _type_: _description_
        """
        if self.img is not None:
            if len(self.img.shape) == 3:
                if channel == 'Y':
                    img_channel = getY(self.img)
                elif channel == 'R':
                    img_channel = self.img[:,:,2]
                elif channel == 'G':
                    img_channel = self.img[:,:,1]
                elif channel == 'B':
                    img_channel = self.img[:,:,0]
            elif len(self.img.shape) == 2:
                if channel == 'Y':
                    img_channel = self.img
            Grad, GradX, GradY = getGrad(img_channel)
            if flag == 0: Grad_img = Grad
            elif flag == 1: Grad_img = GradX
            elif flag == 2: Grad_img = GradY
            grad_pixmap = self.__transform_cvimg_to_pixmap(Grad_img)
            return grad_pixmap
    
    def get_colorchannel_map(self, colormodel, channelflag):
        """_summary_
        Args:
            colormodel (str): 'YUV','HSV'
            channelflag (int): 0,1,2
        Returns:
            _type_: _description_
        """
        if self.img is not None:
            if colormodel == 'YUV':
                img_trans = BGR2YUV(self.img)
            elif colormodel == 'HSV':
                img_trans = BGR2HSV(self.img)
            img_target_channel = img_trans[..., channelflag].copy()
            img_target_channel = pltimshow2cvimg(img_target_channel, False)
            img_target_channel_pixmap = self.__transform_cvimg_to_pixmap(img_target_channel)
            return img_target_channel_pixmap

    def get_frequencydomain_map(self, img, channelname):
        """_summary_
        Args:
            img (arr): 3channel: B G R | 2channel: Gray
            channelname (str): 'R','G','B','Y'
        Returns:
            _type_: _description_
        """
        if len(img.shape) == 3:
            if channelname == 'Y':
                img_channel = getY(img)
            elif channelname == 'R':
                img_channel = img[:,:,2].copy()
            elif channelname == 'G':
                img_channel = img[:,:,1].copy()
            elif channelname == 'B':
                img_channel = img[:,:,0].copy()
        elif len(img.shape) == 2:
            if channelname == 'Y':
                img_channel = img
        freq = getFFT(img_channel)
        fdm = np.log10(np.abs(freq))
        fdm_show = pltimshow2cvimg(noramlization(fdm))
        fdm_pixmap = self.__transform_cvimg_to_pixmap(fdm_show)
        return fdm_pixmap

    def get_frequencydomain_map_global(self, channelname):
        if self.img is not None:
            return self.get_frequencydomain_map(self.img, channelname=channelname)

    def get_frequencydomain_map_ROI(self, channelname):
        if self.img is not None and any(self.index_ROI_real):
            img_roi = self.__get_img_by_index(self.img, self.index_ROI_real)
            return self.get_frequencydomain_map(img_roi, channelname=channelname)

    

    def __update_img(self):
        self.ui.label_img.setPixmap(self.qpixmap)
        self.ui.label_img.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
    

    def __update_text_file_path(self):
        self.ui.label_file_path.setText(f'FilePath: {self.img_path}')

    def __update_text_img_shape(self):
        self.ui.label_img_shape.setText(f'({self.qpixmap.width()}, {self.qpixmap.height()})')
    
    def __update_text_ratio(self):
        self.ui.label_ratio.setText(f'{round(100*self.ratio_rate)}%')
    
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
    
    def __transform_eventpos_to_realpos(self, eventpos_x, eventpos_y):
        real_pos_x = int(eventpos_x / self.qpixmap.width() * self.origin_width)
        real_pos_y = int(eventpos_y / self.qpixmap.height() * self.origin_height)
        return real_pos_x, real_pos_y
    
    def __get_img_by_index(self, img, index):
        """_summary_
        Args:
            img (arr): cv img
            index (list): [upleft_x, upleft_y, dnright_x, dnright_y]
        Returns:
            arr: cropped img
        """
        upleft_x, upleft_y, dnright_x, dnright_y = index
        if len(img.shape) == 3:
            res_img = img[upleft_y:dnright_y, upleft_x:dnright_x, :].copy()
        elif len(img.shape) == 2:
            res_img = img[upleft_y:dnright_y, upleft_x:dnright_x].copy()
        return res_img
    
    def __get_ROI_his_RGBY(self, img, index):
        """_summary_
        Args:
            img (_type_): B G R
            index (LIST): [upleft_x, upleft_y, dnright_x, dnright_y]
        Returns:
            _type_: _description_
        """
        img_roi = self.__get_img_by_index(img, index)
        img_Y_roi = getY(img_roi)
        his = []
        titile_list = ['R','G','B','Y']
        img_rgb_roi = img_roi[..., ::-1].copy()
        for i in range(img.shape[-1]):
            his.append(calcHist(img_rgb_roi[:,:,i]))
        his.append(calcHist(img_Y_roi))
        his_cvimg = plt2cvimg_multisubplots(his, titile_list)
        his_qpixmap = self.__transform_cvimg_to_pixmap(his_cvimg)
        return his_qpixmap