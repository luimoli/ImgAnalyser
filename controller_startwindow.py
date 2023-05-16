import sys
sys

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QHBoxLayout, QFileDialog, QMessageBox

from controller_sm import MyWindow
from controller_mm import MultiModeWindow

from UI.Ui_vistart import Ui_Startup

class StartWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.start_ui = Ui_Startup()
        self.start_ui.setupUi(self)
        self.setup_control()

    def setup_control(self):
        self.start_ui.btn_sm.clicked.connect(self.sm_show)
        self.start_ui.btn_mm.clicked.connect(self.mm_show)
        # self.start_ui.btn_vm.clicked.connect(self.sm_show)

    
    def sm_show(self):
        self.sm = MyWindow()
        self.sm.show()

    def mm_show(self):
        self.mm = MultiModeWindow()
        self.mm.show()