from gettext import translation

import maya.cmds as cmds
import maya.OpenMayaUI as omui
from PySide6 import QtWidgets, QtCore
from shiboken6 import wrapInstance

def get_maya_main_win():
    """Return the Maya main window"""
    main_win_addr = omui.MQtUtil.mainWindow()
    wrapInstance(int(main_win_addr), QtWidgets.QWidget)

# idea: create mesh plane?
# divide mesh into points

# get scatterable objects in scene
def get_objects():
    objects = cmds.ls(geometry=True)
# get location of points and put into a dictionary
def get_points():
    selected_verts = cmds.ls(selection=True, flatten=True)
    vert_positions = {}

    for vert in selected_verts:
        pos = cmds.xform(vert, query=True, worldSpace=True, translation=True)
        vert_positions[vert] = pos

    print(vert_positions[vert])
    
	

# create group of duplicate meshes and place on points
	# use dictionaries to associate mesh with point
# hide duplicate meshes at random based on density slider

if __name__ == "__main__":
    print(cmds.ls(geometry=True))
    # get_points()
