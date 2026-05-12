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
        self.scatter.random_scarcity = self.scarcity_slider.value()
        self.scatter.scatter_cubes()

    def generate_scatter(self):
        self.scatter.random_scarcity = self.scarcity_slider.value()
        self.scatter.scatter_object()

    def _update_scarcity(self):
        self.scatter.random_scarcity = self.scarcity_slider.value()
        self.scatter._update_visibility()

    def _connect_signals(self):
        self.scatter_cubes_btn.clicked.connect(self.generate_cubes)
        self.scatter_on_surface_btn.clicked.connect(self.generate_scatter)

        self.refresh_list_btn.clicked.connect(
            self._refresh_obj_select_combox)
        self.scatter.set_base_object(self.obj_select_combox.currentText())
        self.obj_select_combox.currentTextChanged.connect(
            self.scatter.set_base_object
        )

        self.scarcity_slider.valueChanged.connect(
            self._update_scarcity)
        self.scarcity_slider.valueChanged.connect(
            self.scarcity_slider_number.setValue)
        self.scarcity_slider_number.valueChanged.connect(
            self.scarcity_slider.setValue)

    def _refresh_obj_select_combox(self):
        self.scatter._refresh_list()
        self.obj_select_combox.clear()
        self.obj_select_combox.addItems(self.scatter.obj_list)

    def _mk_main_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self._mk_combox_layout()
        self._mk_buttons_layout()
        self._mk_scarcity_layout()
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

    def _mk_scarcity_layout(self):
        self.scarcity_layout = QtWidgets.QHBoxLayout()
        self.scarcity_slider = QtWidgets.QSlider()
        self.scarcity_slider_lbl = QtWidgets.QLabel("Scarcity")
        self.scarcity_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.scarcity_slider.setValue(50)
        self.scarcity_slider.setMaximum(100)
        self.scarcity_slider.setMinimum(0)

        self.scarcity_slider_number = QtWidgets.QSpinBox()
        self.scarcity_slider_number.setValue(50)
        self.scarcity_slider_number.setMaximum(100)
        self.scarcity_slider_number.setSuffix("%")

        self.scarcity_layout.addWidget(self.scarcity_slider_lbl)
        self.scarcity_layout.addWidget(self.scarcity_slider)
        self.scarcity_layout.addWidget(self.scarcity_slider_number)
        self.main_layout.addLayout(self.scarcity_layout)

    def _mk_buttons_layout(self):
        self.controls_lbl = QtWidgets.QLabel(
            "Scatter Options (Select object to scatter in viewport)")
        self.controls_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.scatter_cubes_btn = QtWidgets.QPushButton("Scatter Cubes")
        self.scatter_on_surface_btn = QtWidgets.QPushButton(
            "Scatter Selection")

        self.main_layout.addWidget(self.controls_lbl)
        self.main_layout.addWidget(self.scatter_cubes_btn)
        self.main_layout.addWidget(self.scatter_on_surface_btn)


class SimpleScatter():

    obj_list = []
    base_object = ""
    random_scarcity = 25
    current_scattered_list = []

    def apply_random_visibility(self):
        scarcity = self.random_scarcity / 100

        scattered_count = len(self.current_scattered_list)
        hidden_count = round(scattered_count * scarcity)

        hidden_list = random.sample(self.current_scattered_list,
                                    hidden_count)

        for obj in hidden_list:
            cmds.hide(obj)

    def scatter_cubes(self):
        self.current_scattered_list = []
        for pos in self.get_points():
            cube = cmds.polyCube(height=0.1,
                                 width=0.1,
                                 depth=0.1,
                                 name="cube")[0]
            cmds.xform(cube, translation=pos)
            self.current_scattered_list.append(cube)
        self.apply_random_visibility()
        grp_name = cmds.group(self.current_scattered_list, name="cubes")
        self._make_child(grp_name)
        return grp_name

    def scatter_object(self):
        self.current_scattered_list = []

        selected_object = cmds.ls(selection=True)[0]
        for pos in self.get_points():
            dupe = cmds.duplicate(selected_object)[0]
            cmds.xform(dupe, translation=pos)
            self.current_scattered_list.append(dupe)
        self.apply_random_visibility()
        grp_name = cmds.group(self.current_scattered_list,
                              name=f"{selected_object}s")
        self._make_child(grp_name)
        return grp_name

    def get_objects(self):
        objects = cmds.ls(geometry=True)
        return objects

    def set_base_object(self, obj_name):
        """Setter for base_object used by the UI combo box signal."""
        self.base_object = obj_name

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

    def _update_visibility(self):
        if self.current_scattered_list:
            cmds.showHidden(self.current_scattered_list)
            self.apply_random_visibility()


if __name__ == "__main__":
    w = ScatterWin()
    w.show()
