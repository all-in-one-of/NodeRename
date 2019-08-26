# PYTHON
import sys
try:
    from PySide2.QtWidgets import *
    from PySide2.QtCore import *
    from PySide2.QtGui import *
except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
# TRIGGERFISH
from utilities.pipeline import system_utils
from modules import core_gui
reload(core_gui)

WINDOW_TITLE = r"Node Rename"


def run():
    data = __get_data(system_utils.get_current_software())
    if data:
        a = core_gui.GuiWindow(parent=data["parent"], software=data["software"], style=data["style"], window_title=WINDOW_TITLE)
        a.show()

def run_stereo():
    data = __get_data(system_utils.get_current_software())
    if data:
        a = core_gui.GuiWindow(parent=data["parent"], software=data["software"], style=data["style"], window_title=WINDOW_TITLE + " - Stereo", stereo=True)
        a.show()


def __get_data(software_name):
    if software_name == "maya":
        from utilities.maya.helper import maya_helper
        reload(maya_helper)
        parent = maya_helper.maya_main_window()
        style = maya_helper.stylesheet()
        software = maya_helper.Helper()
        return {"software": software, "parent": parent, "style": style}
    elif software_name == "houdini":
        from utilities.houdini.helper import houdini_helper
        reload(houdini_helper)
        parent = houdini_helper.houdini_main_window()
        style = houdini_helper.stylesheet()
        software = houdini_helper.Helper()
        return {"software": software, "parent": parent, "style": style}
    return None
    