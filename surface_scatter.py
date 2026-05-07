import maya.cmds as cmds
import maya.OpenMayaUI as omui
from PySide6 import QtWidgets, QtCore
from shiboken6 import wrapInstance


def get_maya_main_win():
    """Return the Maya main window"""
    main_win_addr = omui.MQtUtil.mainWindow()
    wrapInstance(int(main_win_addr), QtWidgets.QWidget)


class ScatterWin(QtWidgets.QDialog):

    def __init__(self):
        super().__init__(parent=get_maya_main_win())
        self.building = SimpleScatter()
        # self.resize(300, 200)
        self.setWindowTitle("Simple Scatter")
        self.setWindowFlags(QtCore.Qt.Tool)
        self._mk_main_layout()
        self._connect_signals()

    def _connect_signals(self):
        pass

    def _mk_main_layout(self):
        pass


class SimpleScatter():

    object_number = 0

    # idea: create mesh plane?

    def get_objects(self):
        objects = cmds.ls(geometry=True)
        selected_object = objects[self.object_number]
        return selected_object

    def get_points(self):
        """Returns a list containing the positions of
        every point in the given object

        Returns:
            list: Vertecies from object.
        """
        obj = self.get_objects()
        object_verts = f"{obj}.vtx[*]"

        selected_verts = cmds.ls(object_verts, flatten=True)

        vert_positions = []
        for vert in selected_verts:
            pos = tuple(cmds.xform(vert,
                                   query=True,
                                   worldSpace=True,
                                   translation=True))
            vert_positions.append(pos)

        return vert_positions

    # create group of duplicate meshes and place on points
    # use dictionaries to associate mesh with point
    # hide duplicate meshes at random based on density slider

    # create group of hidden objects that slider controls
    # allow user to delete hidden objects


if __name__ == "__main__":
    scatter = SimpleScatter()
    print(scatter.get_points())
    for pos in scatter.get_points():
        cube = cmds.polyCube(height=0.01, width=0.01, depth=0.01, name="cube")
        cmds.xform(cube, translation=pos)
