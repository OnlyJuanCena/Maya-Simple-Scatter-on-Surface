import maya.cmds as cmds
import maya.OpenMayaUI as omui
from PySide6 import QtWidgets, QtCore
from shiboken6 import wrapInstance


def get_maya_main_win():
    """Return the Maya main window"""
    main_win_addr = omui.MQtUtil.mainWindow()
    wrapInstance(int(main_win_addr), QtWidgets.QWidget)


class SimpleScatter():

    # idea: create mesh plane?

    def get_objects(self):
        objects = cmds.ls(geometry=True)
        selected_object = objects[0]
        return selected_object

    def get_points(self):
        obj = self.get_objects()
        object_verts = f"{obj}.vtx[*]"

        selected_verts = cmds.ls(object_verts, flatten=True)

        vert_positions = {}
        for vert in selected_verts:
            pos = tuple(cmds.xform(vert,
                                   query=True,
                                   worldSpace=True,
                                   translation=True))
            vert_positions[vert] = pos

        return vert_positions

    # create group of duplicate meshes and place on points
    # use dictionaries to associate mesh with point
    # hide duplicate meshes at random based on density slider


if __name__ == "__main__":
    scatter = SimpleScatter()
    print(scatter.get_points())
