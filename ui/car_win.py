from maya import OpenMayaUI as omui
# from maya.app.general.mayaMixin import MayaQWidgetBaseMixin
from shiboken import wrapInstance
from PySide import QtGui
from carRig.ui import car_ui
from carRig.ui import fill_ui_elem

reload(car_ui)

mayaMainWindowPtr = omui.MQtUtil.mainWindow()
maya_main_window = wrapInstance(long(mayaMainWindowPtr), QtGui.QWidget)


class CarRig(QtGui.QMainWindow, car_ui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(CarRig, self).__init__(parent=parent)
        self.setupUi(self)
        self.connections()

    def connections(self):
        self.fr_wh_L_out_btn.clicked.connect(lambda: fill_ui_elem.filLineEdit(self.fr_wh_L_out_LE))
        self.fr_wh_L_in_btn.clicked.connect(lambda: fill_ui_elem.filLineEdit(self.fr_wh_L_in_LE))
        self.fr_wh_R_out_btn.clicked.connect(lambda: fill_ui_elem.filLineEdit(self.fr_wh_R_out_LE))
        self.fr_wh_R_in_btn.clicked.connect(lambda: fill_ui_elem.filLineEdit(self.fr_wh_R_in_LE))

        self.bk_wh_L_out_btn.clicked.connect(lambda: fill_ui_elem.filLineEdit(self.bk_wh_L_out_LE))
        self.bk_wh_L_in_btn.clicked.connect(lambda: fill_ui_elem.filLineEdit(self.bk_wh_L_in_LE))
        self.bk_wh_R_out_btn.clicked.connect(lambda: fill_ui_elem.filLineEdit(self.bk_wh_R_out_LE))
        self.bk_wh_R_in_btn.clicked.connect(lambda: fill_ui_elem.filLineEdit(self.bk_wh_R_in_LE))


def main():
    winClass = CarRig(maya_main_window)
    return winClass.show()
