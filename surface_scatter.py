import maya.cmds as cmds
import maya.OpenMayaUI as omui
from PySide6 import QtWidgets, QtCore
from shiboken6 import wrapInstance
import random


def get_maya_main_win():
    """Return the Maya main window"""
    main_win_addr = omui.MQtUtil.mainWindow()
    wrapInstance(int(main_win_addr), QtWidgets.QWidget)


class ScatterWin(QtWidgets.QDialog):

    def __init__(self):
        super().__init__(parent=get_maya_main_win())
        self.scatter = SimpleScatter()
        self.scatter.obj_list = self.scatter.get_objects()
        self.setWindowTitle("Simple Scatter")
        self.setWindowFlags(QtCore.Qt.Tool)
        self._mk_main_layout()
        self._connect_signals()

    def _connect_signals(self):
        self.scatter_cubes_btn.clicked.connect(
            self.scatter.scatter_cubes)

        self.refresh_list_btn.clicked.connect(
            self._refresh_obj_select_combox)
        self.scatter.set_base_object(self.obj_select_combox.currentText())
        self.obj_select_combox.currentTextChanged.connect(
            self.scatter.set_base_object
        )

    def _refresh_obj_select_combox(self):
        self.scatter._refresh_list()
        self.obj_select_combox.clear()
        self.obj_select_combox.addItems(self.scatter.obj_list)

    def _mk_main_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self._mk_combox_layout()
        self._mk_buttons_layout()
        self.setLayout(self.main_layout)

    def _mk_combox_layout(self):
        self.obj_select_combox = QtWidgets.QComboBox()
        self.obj_select_combox.addItems(self.scatter.obj_list)

        self.refresh_list_btn = QtWidgets.QPushButton("Refresh List")
        self.main_layout.addWidget(self.obj_select_combox)
        self.main_layout.addWidget(self.refresh_list_btn)

    def _mk_buttons_layout(self):
        self.scatter_cubes_btn = QtWidgets.QPushButton("Scatter Cubes")
        self.main_layout.addWidget(self.scatter_cubes_btn)


class SimpleScatter():

    obj_list = ""
    base_object = ""
    random_placement = True
    random_mult = 70
    random_density = None

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

        for cube in grp_name:
            self.apply_random_visibility(cube)

        self._make_child(grp_name)
        return grp_name

    def apply_random_visibility(self, obj):
        hidden_obj = []
        if self.random_placement is True:
            if random.randint(1, 100) <= self.random_mult:
                cmds.hide(obj)
                hidden_obj.append(obj)

    def get_objects(self):
        objects = cmds.ls(geometry=True)
        print(f"Objects in scene: {objects}")
        return objects

    def set_base_object(self, obj_name):
        """Setter for base_object used by the UI combo box signal."""
        self.base_object = obj_name
        print(f"Base object: {self.base_object}")

    def get_points(self):
        """Returns list containing the positions of
        every point in the given object.

        Returns:
            list: Vertex positions from object.
        """
        vert_positions = []
        object_verts = f"{self.base_object}.vtx[*]"
        verts_list = cmds.ls(object_verts, flatten=True)
        for vert in verts_list:
            pos = tuple(cmds.xform(vert,
                                   query=True,
                                   worldSpace=True,
                                   translation=True))
            vert_positions.append(pos)

        return vert_positions

    def _refresh_list(self):
        self.obj_list = self.get_objects()

    def _make_child(self, obj):
        cmds.parent(obj, self.base_object)

    # create group of duplicate meshes and place on points
    # hide duplicate meshes at random based on density slider

    # create group of hidden objects that slider controls
    # allow user to delete hidden objects


if __name__ == "__main__":
    w = ScatterWin()
    w.show()
