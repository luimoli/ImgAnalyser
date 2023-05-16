from PyQt5 import QtCore 
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtCore import QEvent
from functools import partial

from UI.Ui_vianalyser import Ui_MainWindow
from handler_sm import Handler_sm

from UI.Ui_visecond_single import Ui_MainWindowSecondSingle


class MyWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_second()

        self.setup_control()

    def setup_control(self):
        self.img_controller = Handler_sm(ui=self.ui, ui2=self.ui2)
        self.ui.actionopen_file.triggered.connect(self.open_file)
        # self.ui.btn_zoom_in.clicked.connect(self.img_controller.set_zoom_in)
        # self.ui.btn_zoom_out.clicked.connect(self.img_controller.set_zoom_out)

        self.ui.label_img.installEventFilter(self.ui.label_img)
        self.ui.label_img.eventFilter = self.get_mouse_status
        self.ui.label_img.mouseMoveEvent = self.img_controller.get_move_position
        self.ui.label_img.mousePressEvent = self.img_controller.get_clicked_position
        self.ui.label_img.mouseReleaseEvent = self.img_controller.get_ROI_finished_position
        self.ui.label_img.wheelEvent = self.img_controller.get_wheel_value

        # ROI button
        self.ui.btn_ROI_select.clicked.connect(self.create_ROI)
        self.ui.btn_ROI_clear.clicked.connect(self.img_controller.clear_ROI_img)

        # point button
        self.ui.btn_point_set.clicked.connect(self.create_line)
        self.ui.btn_point_clear.clicked.connect(self.img_controller.clear_line_img)

        self.ui.cbb_distance.currentIndexChanged[int].connect(self.img_controller.calc_line_distance)


        # his and line map generation
        self.ui.actionGlobalHistogram.triggered.connect(self.actionGlobalHistogram_popwindow)
        self.ui.actionROI_Histogram.triggered.connect(self.actionROI_Histogram_popwindow)
        self.ui.actionLine_Histogram.triggered.connect(self.actionLine_Histogram_popwindow)
        self.ui.actionPlotSelectLine.triggered.connect(self.actionPlotSelectLine_popwindow)

        # gradient map
        self.ui.actionGradY_grad.triggered.connect(partial(self.actionGrad_popwindow, 0, 'Y'))
        self.ui.actionGradY_grad_x.triggered.connect(partial(self.actionGrad_popwindow, 1, 'Y'))
        self.ui.actionGradY_grad_y.triggered.connect(partial(self.actionGrad_popwindow, 2, 'Y'))

        self.ui.actionGradR_grad.triggered.connect(partial(self.actionGrad_popwindow, 0, 'R'))
        self.ui.actionGradR_grad_x.triggered.connect(partial(self.actionGrad_popwindow, 1, 'R'))
        self.ui.actionGradR_grad_y.triggered.connect(partial(self.actionGrad_popwindow, 2, 'R'))

        self.ui.actionGradG_grad.triggered.connect(partial(self.actionGrad_popwindow, 0, 'G'))
        self.ui.actionGradG_grad_x.triggered.connect(partial(self.actionGrad_popwindow, 1, 'G'))
        self.ui.actionGradG_grad_y.triggered.connect(partial(self.actionGrad_popwindow, 2, 'G'))

        self.ui.actionGradB_grad.triggered.connect(partial(self.actionGrad_popwindow, 0, 'B'))
        self.ui.actionGradB_grad_x.triggered.connect(partial(self.actionGrad_popwindow, 1, 'B'))
        self.ui.actionGradB_grad_y.triggered.connect(partial(self.actionGrad_popwindow, 2, 'B'))

        # color channel
        self.ui.actionHSV_H_channel.triggered.connect(partial(self.actionColorChannel_popwindow, 'HSV', 0))
        self.ui.actionHSV_S_channel.triggered.connect(partial(self.actionColorChannel_popwindow, 'HSV', 1))
        self.ui.actionHSV_V_channel.triggered.connect(partial(self.actionColorChannel_popwindow, 'HSV', 2))

        self.ui.actionYUV_Y_channel.triggered.connect(partial(self.actionColorChannel_popwindow, 'YUV', 0))
        self.ui.actionYUV_U_channel.triggered.connect(partial(self.actionColorChannel_popwindow, 'YUV', 1))
        self.ui.actionYUV_V_channel.triggered.connect(partial(self.actionColorChannel_popwindow, 'YUV', 2))

        # FDD
        self.ui.actionGlobal_FD_R.triggered.connect(partial(self.actionFD_Global_popwindow, 'R'))
        self.ui.actionGlobal_FD_G.triggered.connect(partial(self.actionFD_Global_popwindow, 'G'))
        self.ui.actionGlobal_FD_B.triggered.connect(partial(self.actionFD_Global_popwindow, 'B'))
        self.ui.actionGlobal_FD_Y.triggered.connect(partial(self.actionFD_Global_popwindow, 'Y'))

        self.ui.actionFD_ROI_R.triggered.connect(partial(self.actionFD_ROI_popwindow, 'R'))
        self.ui.actionFD_ROI_G.triggered.connect(partial(self.actionFD_ROI_popwindow, 'G'))
        self.ui.actionFD_ROI_B.triggered.connect(partial(self.actionFD_ROI_popwindow, 'B'))
        self.ui.actionFD_ROI_Y.triggered.connect(partial(self.actionFD_ROI_popwindow, 'Y'))


        # neighbor 
        # self.ui.spinBox_range.valueChanged.connect()
        self.ui.cbb_neib_show.currentIndexChanged[int].connect(self.neib_popwindow)

    def setup_second(self):
        self.form = QMainWindow()
        self.ui2 = Ui_MainWindowSecondSingle()
        self.ui2.setupUi(self.form)

    #-------------menu bar----------------------------------------------------------
    def set_ui2_pixmap_show(self, pixmap):
        self.ui2.label_map.setPixmap(pixmap)
        self.ui2.label_map.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.form.show()
    
    def neib_popwindow(self, index):
        if index:
            self.form.show()

    def actionGlobalHistogram_popwindow(self):
        pixmap = self.img_controller.get_global_his()
        if pixmap: self.set_ui2_pixmap_show(pixmap)

    def actionROI_Histogram_popwindow(self):
        pixmap = self.img_controller.get_ROI_his()
        if pixmap: self.set_ui2_pixmap_show(pixmap)

    def actionLine_Histogram_popwindow(self):
        pixmap = self.img_controller.get_Line_his()
        if pixmap: self.set_ui2_pixmap_show(pixmap)

    def actionPlotSelectLine_popwindow(self):
        pixmap = self.img_controller.get_Line_plot()
        if pixmap: self.set_ui2_pixmap_show(pixmap)
    
    def actionGrad_popwindow(self, flag, channel):
        pixmap = self.img_controller.get_gradient_map(flag=flag, channel=channel)
        if pixmap: self.set_ui2_pixmap_show(pixmap)

    def actionColorChannel_popwindow(self, colormodel, channelflag):
        pixmap = self.img_controller.get_colorchannel_map(colormodel=colormodel,channelflag=channelflag)
        if pixmap: self.set_ui2_pixmap_show(pixmap)

    def actionFD_Global_popwindow(self, channelname):
        pixmap = self.img_controller.get_frequencydomain_map_global(channelname=channelname)
        if pixmap: self.set_ui2_pixmap_show(pixmap)

    def actionFD_ROI_popwindow(self, channelname):
        pixmap = self.img_controller.get_frequencydomain_map_ROI(channelname=channelname)
        if pixmap: self.set_ui2_pixmap_show(pixmap)
    

    #------------------------------------------------------------------------------------------------
    def open_file(self):
        filename, filetype = QFileDialog.getOpenFileName(self, "Open file", "./") # start path   
        if filename:
            # self.ui.slider_zoom.setProperty("value", 50)
            self.img_controller.set_img_path(filename)
            # self.ui.slider_zoom.valueChanged.connect(self.img_controller.get_slider_value)

    def get_mouse_status(self, object, event):
        if event.type() == QEvent.Enter: # 当鼠标进入时
            self.img_controller.mouse_in = True
            # print('Mouse is over the label, Object Text, {}'.format(object.text()))
            return True
        elif event.type() == QEvent.Leave: # 当鼠标离开时
            # print('Mouse is not over the label')
            self.img_controller.mouse_in = False
            self.img_controller.stop_cursor_RGB()

        return False

    def create_line(self):
        if self.img_controller.mode_line:
            self.ui.btn_point_set.setText('line set')
            self.img_controller.mode_line = False

        else:
            self.ui.btn_point_set.setText('STOP')
            self.img_controller.mode_line = True

    def create_ROI(self):
        if self.img_controller.mode_ROI:
            self.ui.btn_ROI_select.setText('ROI select')
            self.img_controller.mode_ROI = False
        else:
            self.ui.btn_ROI_select.setText('STOP')
            self.img_controller.mode_ROI = True


    # def show_event(self, event):
    #     print(f"[show_mouse] {event.x()=}, {event.y()=}")


    
    # def read_img_and_show(self, file_path):
    #     pixmap = QPixmap(file_path)
    #     width, height = pixmap.width(), pixmap.height()
    #     # fixheight = height / (width / fixwidth)
    #     self.ui.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 70, math.ceil(width), math.ceil(height)))
    #     self.ui.label_2.setPixmap(pixmap)
    #     self.resize(width+200, height+200)


    # def read_img_opencv(self, file_path):
    #     pixmap = cv2.imread(file_path)[:,:,::-1].copy()
    #     # pixmap = cv2.resize(pixmap, (800, 600), interpolation=cv2.INTER_CUBIC)
    #     height, width = pixmap.shape[:2]
    #     img_qi = QImage(pixmap, pixmap.shape[1],pixmap.shape[0],pixmap.shape[1]*3, QImage.Format_RGB888)
    #     img_pixmap = QPixmap(img_qi)
    #     self.ui.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 90, width, height))
    #     self.ui.label_2.setPixmap(img_pixmap)
    #     self.resize(width+200, height+200)


    

    





    # def msg(self):
    #     fileName1, filetype = QFileDialog.getOpenFileName(self,"","./","All Files (*);;JPG Files (*.jpg);;PNG Files (*.png)")
    #     if fileName1:
    #         try:
    #             self.read_img_opencv(fileName1)
    #         except Exception as e:
    #             self.msgCritical(str(e))

    # def msgCritical(self, strInfo):
    #     dlg = QMessageBox()
    #     dlg.setIcon(QMessageBox.Critical)
    #     dlg.setText(strInfo)
    #     dlg.show()