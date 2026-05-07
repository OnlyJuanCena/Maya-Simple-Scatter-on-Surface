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
    print(f"Selected objects = {objects}")
    return objects[0]


# get location of points and put into a dictionary
def get_points():
    object = get_objects()
    object_verts = f"{object}.vtx[*]"

    selected_verts = cmds.ls(object_verts, flatten=True)
    print(f"Object Verts = {selected_verts}")
    print(f"Type = {type(selected_verts)}")

    vert_positions = {}
    for vert in selected_verts:
        pos = tuple(cmds.xform(vert,
                               query=True,
                               worldSpace=True,
                               translation=True))
        vert_positions[vert] = pos

    # cmds.select(vert_positions[30])
    print(vert_positions["pPlane1.vtx[37]"])
    print(type(vert_positions["pPlane1.vtx[37]"]))

# create group of duplicate meshes and place on points
# use dictionaries to associate mesh with point
# hide duplicate meshes at random based on density slider


if __name__ == "__main__":
    # get_objects()
    get_points()
