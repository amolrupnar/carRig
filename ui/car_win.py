from maya import OpenMayaUI as omui
# from maya.app.general.mayaMixin import MayaQWidgetBaseMixin
from shiboken import wrapInstance
from PySide import QtGui
from carRig.ui import car_ui
from carRig.ui import fill_ui_elem
from carRig.mods import wheel

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
        # create button command add
        self.create_btn.clicked.connect(self.createRig)

    def createRig(self):
        # with fill_ui_elem.UndoChunkOpen('wheel rig'):
        # front wheel left rig.
        fr_wh_L_out = self.fr_wh_L_out_LE.text()
        fr_wh_L_in = self.fr_wh_L_in_LE.text()
        wheel.addStretchRig(fr_wh_L_in, fr_wh_L_out, 'FrontWheelAxel', '_L', 'Main')
        # front wheel right rig.
        fr_wh_R_out = self.fr_wh_R_out_LE.text()
        fr_wh_R_in = self.fr_wh_R_in_LE.text()
        wheel.addStretchRig(fr_wh_R_in, fr_wh_R_out, 'FrontWheelAxel', '_R', 'Main')
        # Back wheel left rig.
        bk_wh_L_out = self.bk_wh_L_out_LE.text()
        bk_wh_L_in = self.bk_wh_L_in_LE.text()
        wheel.addStretchRig(bk_wh_L_in, bk_wh_L_out, 'BackWheelAxel', '_L', 'Main')
        # Back wheel right rig.
        bk_wh_R_out = self.bk_wh_R_out_LE.text()
        bk_wh_R_in = self.bk_wh_R_in_LE.text()
        wheel.addStretchRig(bk_wh_R_in, bk_wh_R_out, 'BackWheelAxel', '_R', 'Main')


def main():
    winClass = CarRig(maya_main_window)
    return winClass.show()
