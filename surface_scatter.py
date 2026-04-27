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

# get objects in scene that can be scattered on
def get_objects():
    objects = cmds.ls(geometry=True)
    return objects[1]

# get location of points and put into a dictionary
def get_points():

    selected_verts = cmds.ls(selection=True, flatten=True)

    if len(cmds.ls(selection=True)) == 0:
        print("You need to select an object or group first.")

    vert_positions = {}
    for vert in selected_verts:
        pos = cmds.xform(vert, query=True, worldSpace=True, translation=True)
        vert_positions[vert] = pos

    print(vert_positions)
    
	

# create group of duplicate meshes and place on points
	# use dictionaries to associate mesh with point
# hide duplicate meshes at random based on density slider

if __name__ == "__main__":
    # get_objects()
    get_points()
