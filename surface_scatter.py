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

    def generate_cubes(self):
        self.scatter.random_density = self.density_slider.value()
        self.scatter.scatter_cubes()

    def _connect_signals(self):
        self.scatter_cubes_btn.clicked.connect(self.generate_cubes)

        self.refresh_list_btn.clicked.connect(
            self._refresh_obj_select_combox)
        self.scatter.set_base_object(self.obj_select_combox.currentText())
        self.obj_select_combox.currentTextChanged.connect(
            self.scatter.set_base_object
        )

        self.density_slider.valueChanged.connect(
            self.density_slider_number.setValue)
        self.density_slider_number.valueChanged.connect(
            self.density_slider.setValue)

    def _refresh_obj_select_combox(self):
        self.scatter._refresh_list()
        self.obj_select_combox.clear()
        self.obj_select_combox.addItems(self.scatter.obj_list)

    def _mk_main_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self._mk_combox_layout()
        self._mk_buttons_layout()
        self._mk_density_layout()
        self.setLayout(self.main_layout)

    def _mk_combox_layout(self):
        self.combox_lbl = QtWidgets.QLabel("Base Object")
        self.combox_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.main_layout.addWidget(self.combox_lbl)

        self.combox_layout = QtWidgets.QHBoxLayout()
        self.obj_select_combox = QtWidgets.QComboBox()
        self.obj_select_combox.addItems(self.scatter.obj_list)

        self.refresh_list_btn = QtWidgets.QPushButton("Refresh List")
        self.combox_layout.addWidget(self.obj_select_combox)
        self.combox_layout.addWidget(self.refresh_list_btn)
        self.main_layout.addLayout(self.combox_layout)

    def _mk_density_layout(self):
        self.density_layout = QtWidgets.QHBoxLayout()
        self.density_slider = QtWidgets.QSlider()
        self.density_slider_lbl = QtWidgets.QLabel("Density")
        self.density_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.density_slider.setValue(50)
        self.density_slider.setMaximum(100)
        self.density_slider.setMinimum(0)

        self.density_slider_number = QtWidgets.QSpinBox()
        self.density_slider_number.setValue(50)
        self.density_slider_number.setMaximum(100)
        self.density_slider_number.setSuffix("%")

        self.density_layout.addWidget(self.density_slider_lbl)
        self.density_layout.addWidget(self.density_slider)
        self.density_layout.addWidget(self.density_slider_number)
        self.main_layout.addLayout(self.density_layout)

    def _mk_buttons_layout(self):
        self.scatter_cubes_btn = QtWidgets.QPushButton("Scatter Cubes")
        self.main_layout.addWidget(self.scatter_cubes_btn)


class SimpleScatter():

    obj_list = ""
    base_object = ""
    random_placement = True
    random_density = 25
    hidden_list = []

    def scatter_cubes(self):
        cube_names = []

        for pos in self.get_points():
            cube = cmds.polyCube(height=0.1,
                                 width=0.1,
                                 depth=0.1,
                                 name="cube")[0]
            cmds.xform(cube, translation=pos)
            cube_names.append(cube)

        self.apply_random_visibility(cube_names)

        grp_name = cmds.group(cube_names, name="cubes")

        self._make_child(grp_name)
        return grp_name

    def apply_random_visibility(self, objects):
        if self.random_placement is True:
            density = self.random_density / 100
            print(f"Density: {density}")

            hidden_count = round(len(objects) * density)
            hidden_count = max(0, min(hidden_count, len(objects)))

            self.hidden_list = (
                random.sample(objects, hidden_count)
                if hidden_count else []
            )

            for obj in self.hidden_list:
                cmds.hide(obj)

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
