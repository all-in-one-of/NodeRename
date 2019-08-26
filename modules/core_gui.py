# PYTHON
import os
import re
import sys
try:
    from PySide2.QtWidgets import *
    from PySide2.QtCore import *
    from PySide2.QtGui import *
except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
from pprint import pprint
from functools import partial
# SOFTWARE
# TRIGGERFISH
import hou
import rn_utils
reload(rn_utils)


# SETTINGS ======================================================
STATIC_DIRECTORY = os.path.abspath(
    os.path.join(__file__, "../..", "resources"))
IMAGE_DIRECTORY = os.path.join(STATIC_DIRECTORY, "img")

MAIN_WINDOW_SIZE = {"width": 400, "height": 420}
# SETTINGS END==================================================


class GuiWindow(QWidget):
    def __init__(self, parent, software, style, window_title, stereo=False):
        super(GuiWindow, self).__init__(parent)

        self.isStereo = stereo
        self.windowStyle = style
        self.windowTitle = window_title

        self.software = software
        self.onlyInt = QIntValidator()

        self.captureGroups = {}

        self.conversionRadios = []

        self.conversionRadioGroup = None

        self.__build_window()

        self.__add_widgets()
        self.setStyleSheet(self.windowStyle)
        self.debug = True

    def __build_window(self):
        self.setWindowTitle(self.windowTitle)
        self.setWindowFlags(Qt.Tool)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.vbMain = QVBoxLayout()
        self.vbMain.addStretch(1)
        self.setFixedSize(
            MAIN_WINDOW_SIZE["width"], MAIN_WINDOW_SIZE["height"])

    def __add_banner(self):
        # create widget items
        pic = QLabel(self)
        if self.isStereo:
            pic.setPixmap(QPixmap(os.path.join(
                IMAGE_DIRECTORY, "banner_stereo.png")))
        else:
            pic.setPixmap(QPixmap(os.path.join(IMAGE_DIRECTORY, "banner.png")))
        # pic.setFixedSize(MAIN_WINDOW_SIZE["width"], 85)
        pic.move(0, 0)
        return pic

    def __add_widgets(self):
        layout = QVBoxLayout()
        # layout.addWidget(self.__add_banner())
        lblActNode = QLabel("Active node", self)
        lblActNode.setStyleSheet(
            ".QLabel{color: white; font-size: 18px; font-weight: bold;}")
        lblActNode.setAlignment(Qt.AlignCenter)
        layout.addWidget(lblActNode)

        self.lblSelected = QLabel(self.__get_selected_node(), self)
        self.lblSelected.setStyleSheet(
            ".QLabel{color: white; font-size: 18px; font-weight: bold;}")
        self.lblSelected.setAlignment(Qt.AlignCenter)


        lblDesNodeName = QLabel("Enter desired name:", self)
        lblDesNodeName.setFixedSize(200, 40)
        lblDesNodeName.move(10, 270)
        lblDesNodeName.setStyleSheet(
            ".QLabel{color: white; font-size: 18px; font-weight: bold;}")
        self.lneNewNodeName = QLineEdit("", self)
        self.lneNewNodeName.setFixedHeight(40)
        self.lneNewNodeName.setAlignment(Qt.AlignCenter)
        self.lneNewNodeName.setStyleSheet(
            ".QLineEdit{background-color: #19191f; color: white; font-size: 14px; font-weight: bold;}")
        self.lneNewNodeName.textChanged.connect(self.__update_output)
        self.lblDesOut = QLabel("", self)
        self.lblDesOut.setStyleSheet(
            ".QLabel{color: white; font-size: 18px; font-weight: bold;}")
        self.lblDesOut.setAlignment(Qt.AlignCenter)

        layout.addWidget(lblDesNodeName)
        layout.addWidget(self.lneNewNodeName)
        layout.addWidget(self.lblDesOut)

        self.btnRename = QPushButton("", self)
        self.btnRename.setFixedSize(MAIN_WINDOW_SIZE["width"]-20, 40)
        self.btnRename.move(10, 370)
        self.btnRename.defaultText = "Rename Node"
        self.btnRename.busyText = "Please Wait"
        self.btnRename.setText(self.btnRename.defaultText)
        self.btnRename.defaultStyle = ".QPushButton{background: #617c36; color: white; font-size: 18px; border-radius: 0px;}.QPushButton:hover{background: #779c3d;}.QPushButton:pressed{background: #39491f;}"
        self.btnRename.busyStyle = ".QPushButton{background: #4d59b0; color: white; font-size: 18px; border-radius: 0px;}"
        self.btnRename.setStyleSheet(self.btnRename.defaultStyle)
        self.btnRename.clicked.connect(self.__run_renaming)
        layout.addWidget(self.btnRename)

        self.setLayout(layout)

    def __update_output(self):
        self.lblDesOut.setText(rn_utils.validate_name(self.lneNewNodeName.text()))

    def __toggle_button_style(self, toggle_button, set_state=None):
        _state = toggle_button.isOn
        if set_state != None:
            _state = set_state

        if _state == True:
            toggle_button.isOn = False
            toggle_button.setText("HUD\nOff")
            _style = ".QPushButton{background: #b14444;}.QPushButton:hover{background: #c94e4e;}.QPushButton:pressed{background: #883636;}"
        elif _state == False:
            toggle_button.isOn = True
            toggle_button.setText("HUD\nOn")
            _style = ".QPushButton{background: #3f89a8;}.QPushButton:hover{background: #4ca6cb;}.QPushButton:pressed{background: #2e6881;}"
        toggle_button.setStyleSheet(_style)

    def __get_selected_node(self):
        nds = hou.selectedItems()
        if nds:
            return nds[0].path()
        return ""

    def __run_renaming(self):
        ndp = self.lblSelected.text()
        nd = hou.node(ndp)
        nd.setName(self.lblDesOut.text(), 1)
