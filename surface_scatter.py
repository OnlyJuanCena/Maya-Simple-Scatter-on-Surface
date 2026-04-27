import maya.cmds as cmds
import maya.OpenMayaUI as omui
from PySide6 import QtWidgets, QtCore
from shiboken6 import wrapInstance

def get_maya_main_win():
    """Return the Maya main window"""
    main_win_addr = omui.MQtUtil.mainWindow()
    wrapInstance(int(main_win_addr), QtWidgets.QWidget)

# create mesh plane?
# divide mesh into points
# get location of points and put into a list
# create group of duplicate meshes and place on points
	# use dictionaries to associate mesh with point
# hide duplicate meshes at random based on density slider
