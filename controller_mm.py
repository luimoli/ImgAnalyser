from PyQt5.QtWidgets import QMainWindow, QFileDialog
from functools import partial
from PyQt5 import QtCore 


from handler_mm import Handler_mm
from UI.Ui_vianalyser_cmp import Ui_MainWindowMultiMode
from UI.Ui_visecond_single import Ui_MainWindowSecondSingle

class MultiModeWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindowMultiMode()
        self.ui.setupUi(self)
        self.setup_second_window()
        self.setup_control()

    def setup_control(self):
        self.handler_mm = Handler_mm(self.ui)
        self.ui.actionOpen_Files.triggered.connect(self.open_files)
        self.ui.label_img1.wheelEvent = self.handler_mm.get_wheel_value
        self.ui.label_img2.wheelEvent = self.handler_mm.get_wheel_value
        self.ui.actionSSIM.triggered.connect(partial(self.handler_mm.calc_metric, 'SSIM'))
        self.ui.actionPSNR.triggered.connect(partial(self.handler_mm.calc_metric, 'PSNR'))
        self.ui.actionDiff_R_Map.triggered.connect(partial(self.actionDiffMap_popwindow, 'R'))
        self.ui.actionDiff_G_Map.triggered.connect(partial(self.actionDiffMap_popwindow, 'G'))
        self.ui.actionDiff_B_Map.triggered.connect(partial(self.actionDiffMap_popwindow, 'B'))
        self.ui.actionDiff_Y_Map.triggered.connect(partial(self.actionDiffMap_popwindow, 'Y'))


    def setup_second_window(self):
        self.form = QMainWindow()
        self.ui2 = Ui_MainWindowSecondSingle()
        self.ui2.setupUi(self.form)

    def set_ui2_pixmap_show(self, pixmap):
        self.ui2.label_map.setPixmap(pixmap)
        self.ui2.label_map.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.form.show()
    
    def actionDiffMap_popwindow(self, channelname):
        pixmap = self.handler_mm.get_diff_map(channelname=channelname)
        if pixmap: self.set_ui2_pixmap_show(pixmap)

    def open_files(self):
        filenames, filetype = QFileDialog.getOpenFileNames(self, "Open file", "./") # start path  
        if len(filenames) == 2:
            self.handler_mm.set_img_path(filenames)
    
        
