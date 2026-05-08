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
        self.scatter = SimpleScatter()
        self.setWindowTitle("Simple Scatter")
        self.setWindowFlags(QtCore.Qt.Tool)
        self._mk_main_layout()
        self._connect_signals()

    def _connect_signals(self):
        self.scatter_cubes_btn.clicked.connect(
            self.scatter.scatter_cubes)
        self.obj_select_combox.currentTextChanged.connect(
            self.scatter.base_object
        )

    def _mk_main_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self._mk_combox_layout()
        self._mk_buttons_layout()
        self.setLayout(self.main_layout)

    def _mk_combox_layout(self):
        self.obj_select_combox = QtWidgets.QComboBox()
        self.obj_select_combox.addItems(self.scatter.get_objects())
        self.main_layout.addWidget(self.obj_select_combox)

    def _mk_buttons_layout(self):
        self.scatter_cubes_btn = QtWidgets.QPushButton("Scatter Cubes")
        self.main_layout.addWidget(self.scatter_cubes_btn)


class SimpleScatter():

    obj_list = ""
    base_object = ""

    def scatter_cubes(self):
        cube_names = []

        for pos in self.get_points():
            cube = cmds.polyCube(height=0.1,
                                 width=0.1,
                                 depth=0.1,
                                 name="cube")[0]
            cmds.xform(cube, translation=pos)
            cube_names.append(cube)

        grp_name = cmds.group(cube_names, name="cubes")
        self._make_child(grp_name)
        return grp_name

    def get_objects(self):
        objects = cmds.ls(geometry=True)
        return objects

    def get_base_object(self):
        if self.base_object == "":
            return self.get_objects()[0]
        else:
            return self.base_object

    def get_points(self):
        """Returns a list containing the positions of
        every point in the given object

        Returns:
            list: Vertecies from object.
        """

        self.base_object = self.get_base_object()
        print(f"{self.base_object}")
        object_verts = f"{self.base_object}.vtx[*]"
        print(f"{object_verts}")

        selected_verts = cmds.ls(object_verts, flatten=True)
        print(selected_verts)

        vert_positions = []
        for vert in selected_verts:
            pos = tuple(cmds.xform(vert,
                                   query=True,
                                   worldSpace=True,
                                   translation=True))
            vert_positions.append(pos)

        return vert_positions

    def _make_child(self, obj):
        cmds.setParent(obj, self.get_base_object())

    def _freeze_transforms(self, obj):
        cmds.makeIdentity(obj, apply=True, translate=True, rotate=True,
                          scale=True, normal=False, preserveNormals=True)

    def _set_pivot_to_origin(self, obj):
        cmds.xform(obj, pivots=[0, 0, 0])

    # create group of duplicate meshes and place on points
    # use dictionaries to associate mesh with point
    # hide duplicate meshes at random based on density slider

    # create group of hidden objects that slider controls
    # allow user to delete hidden objects


if __name__ == "__main__":
    w = ScatterWin()
    w.show()
