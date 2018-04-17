"""
Name: gui.py
Author: Sam O
Date: 4/22/18

Info:
This file is where PyQt5 gui code is made

"""


# Imports
import PyQt5.QtWidgets as widget
import util
import matplotlib.pyplot as plt
import sys


# Other Imports
# import matplotlib.path as path
# import matplotlib.patches as patches
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
# import matplotlib.image as m_image
# import PIL.Image as image
# import numpy as np
# import math
# import os
import sys
import PyQt5.QtWidgets as widget
# import PyQt5.QtGui as gui
# import PyQt5.QtCore as core


class Visualizer(FigureCanvas):
    # https://pythonspot.com/pyqt5-matplotlib/
    def __init__(self, parent=None, width=5, height=4, dpi=100, fig=None):
        fig = fig

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.updateGeometry(self)
        self.plot()

    def plot(self):
        data = []
        for entry in data:
            if entry.get_visible():
                entry.draw()

        self.draw()




















class CurveEntry(widget.QCheckBox):
    def __init__(self, parent=None, name="No name", width=5, height=4, curve=None):
        # CurveEntry.__init__(parent=parent, name=name, width=width, height=height, curve=curve)
        #super(CurveEntry).__init__()
        self.parent = parent
        self.name = name
        self.width = width
        self.height = height
        self.curve = curve

        self.label = widget.QLabel(self.parent)
        self.label.setText(self.name)

        self.visible_check = widget.QCheckBox(self.parent)

        # self.select_button = widget.QPushButton(self.parent)
        # self.select_button.setCheckable(True)
        # self.select_button.setDown(False)
        self.select = widget.QRadioButton(self.parent)

        self.x, self.y = 0, 0

    def move(self, *__args):
        x = __args[0]
        y = __args[1]
        self.label.move(x + 4 * self.width, y)
        self.visible_check.move(x, y)
        self.select.move(x + 15 * self.width, y)
        self.x = x + 4 * self.width
        self.y = y

    def isCurveVisible(self):
        return self.visible_check.isChecked()

    def setCurveVisible(self, bool):
        self.curve.set_visible(bool)
        self.visible_check.setCheckState(bool)

    def getCurve(self):
        return self.curve

    def setCurve(self, new_curve):
        self.curve = new_curve

    # def addSelectWidget(self, qwidget):
    #     self.select = qwidget
    #     self.select.move(self.x + 60, self.y)

    def getSelected(self):
        return self.select.isChecked()

    def connectChecked(self, func):
        self.select.toggled.connect(func)























class CurvePathGenerator():
    def __init__(self):
        self.dim = [1000, 700]  # Set Dimensions with list ----> Personal preference

        self.starting_positions = {"Center": [90, (324 // 2) - 12],
                                   "Left": [90, 67],
                                   "Right": [90, 257]}
        self.path_colors = {0: (0, 0, 0, 1),
                            1: (1, 0, 0, 1),
                            2: (0, 1, 0, 1),
                            3: (0, 0, 1, 1),
                            4: (1, 1, 0, 1),
                            5: (1, 0, 1, 1),
                            6: (0, 1, 1, 1),
                            7: (1, 1, 1, 1),
                            8: (0.6, 0.6, 0.6, 1),
                            9: (0.3, 0.3, 0.3, 1)}

        self.color_path_count = 0

        # Vertices list
        self.verts = [(0, 0),
                      (50, 0),
                      (0, 50),
                      (100, 50)]
        self.default_verts = [(0, 0),
                              (50, 0),
                              (0, -50),
                              (100, -50)]

        self.using_raw_rpappa_coords = False
        self.image_overlay_exists = False

        # Path to image
        self.image_location = 'overlay.png'
        self.image_overlay_exists = util.check_file_exists(self.image_location)

        # Path to output file
        self.text_location = 'code.txt'

        # Curves List
        self.curves = []
        self.curve_limit = 8
        self.curve_selected = None

        # Matplotlib vars
        self.fig = None
        self.ax = None
        self.overlay = None

        # PyQt5 vars
        self.window = None

        self.create_fig()
        self.create_gui()



    # Setups gui
    def create_gui(self):
        self.window = widget.QWidget()  # Create window
        self.window.setWindowTitle("Curve Path Generator")  # Set window Title
        self.window.setGeometry(100, 200, self.dim[0], self.dim[1])  # Set window position and size
        #self.window.setWindowIcon(gui.QIcon('src\\icon.ico'))  # Set window icon
        self.window.setStyle(widget.QStyleFactory.create("Fusion"))  # set Style

        # Visualizer (Matplotlib figure)
        self.vis = Visualizer(parent=self.window, fig=self.fig)
        vis_w, vis_h = self.vis.get_width_height()
        # vis.move(self.dim[0] // 2 - vis_w // 2, self.dim[1]//2 - vis_h // 2)
        self.vis.move(50, 30)


        self.update_button = widget.QPushButton(self.window)
        self.update_button.setText("Update")
        self.update_button.clicked.connect(self.update_gui)
        self.update_button.move(0, 650)



        self.create_coord_entries()
        self.create_curve_entries()
        self.create_coord_system_selection()
        self.create_starting_position_selection()
        self.vis.plot()

    # Create starting position frame and selection widgets
    def create_starting_position_selection(self):
        self.starting_pos_frame = widget.QFrame(self.window)
        self.starting_pos_frame.setFrameShape(widget.QFrame.StyledPanel)
        vertical_layout = widget.QVBoxLayout(self.starting_pos_frame)

        starting_group = widget.QButtonGroup(vertical_layout)

        starting_center = widget.QRadioButton(self.starting_pos_frame)
        starting_left = widget.QRadioButton(self.starting_pos_frame)
        starting_right = widget.QRadioButton(self.starting_pos_frame)

        starting_center.setText("Center")
        starting_right.setText("Right")
        starting_left.setText("Left")

        starting_group.addButton(starting_center)
        starting_group.addButton(starting_left)
        starting_group.addButton(starting_right)

        vertical_layout.addWidget(starting_left)
        vertical_layout.addWidget(starting_right)
        vertical_layout.addWidget(starting_center)

        self.starting_pos_frame.move(0, 120)
        starting_left.toggled.connect(lambda x: self.change_start("Left"))
        starting_right.toggled.connect(lambda x: self.change_start("Right"))
        starting_center.toggled.connect(lambda x: self.change_start("Center"))

    # Create coordinate system position frame and selection widgets
    def create_coord_system_selection(self):
        self.coord_sys_frame = widget.QFrame(self.window)
        self.coord_sys_frame.setFrameShape(widget.QFrame.StyledPanel)
        vertical_layout = widget.QVBoxLayout(self.coord_sys_frame)
        coord_sys_group = widget.QButtonGroup(vertical_layout)

        rpappa_coord = widget.QRadioButton(self.coord_sys_frame)
        native_coord = widget.QRadioButton(self.coord_sys_frame)

        vertical_layout.addWidget(rpappa_coord)
        vertical_layout.addWidget(native_coord)

        rpappa_coord.setText("Rpappa Coord")
        native_coord.setText("Native Coord")

        coord_sys_group.addButton(rpappa_coord)
        coord_sys_group.addButton(native_coord)

        self.coord_sys_frame.move(0, 40)
        rpappa_coord.toggled.connect(lambda x: self.change_coord_system(True))
        native_coord.toggled.connect(lambda x: self.change_coord_system(False))

    # Creates coord entries
    def create_coord_entries(self):

        start_x = widget.QLineEdit(self.window)
        start_y = widget.QLineEdit(self.window)
        mid1_x = widget.QLineEdit(self.window)
        mid1_y = widget.QLineEdit(self.window)
        mid2_x = widget.QLineEdit(self.window)
        mid2_y = widget.QLineEdit(self.window)
        end_x = widget.QLineEdit(self.window)
        end_y = widget.QLineEdit(self.window)

        self.text_entries = [[start_x, start_y, mid1_x, mid1_y], [end_x, end_y, mid2_x, mid2_y]]
        for y in range(2):
            for x in range(4):
                self.text_entries[y][x].move(x * 200, (y * 50) + 550)

        # self.main_grid.addWidget(start_x, 0, 0)
        # self.main_grid.addWidget(start_y, 0, 1)
        # self.main_grid.addWidget(mid1_x, 0, 2)
        # self.main_grid.addWidget(mid1_y, 0, 3)
        # self.main_grid.addWidget(mid2_x, 2, 0)
        # self.main_grid.addWidget(mid2_y, 2, 1)
        # self.main_grid.addWidget(end_x, 2, 2)
        # self.main_grid.addWidget(end_y, 2, 3)
        start_x.setText("Startx")
        start_y.setText("Starty")
        mid1_x.setText("Mid1x")
        mid1_y.setText("Mid1y")
        mid2_x.setText("Mid2x")
        mid2_y.setText("Mid2y")
        end_x.setText("Endx")
        end_y.setText("Endy")

    # Creates all the curve entries
    def create_curve_entries(self):
        self.curve_entries = []
        for y in range(self.curve_limit):
            # self.curve_entries[y] = widget.QCheckBox(self.window)
            # self.curve_entries[y].setText("Curve " + str(y))
            # self.curve_entries[y].move(750, y * 50 + 100)
            self.curve_entries.append(CurveEntry(parent=self.window, name="Curve " + str(y)))
            self.curve_entries[y].move(750, y * 50 + 100)
            self.curve_entries[y].connectChecked(lambda x: self.select(self.curve_entries[y]))
        self.create_curves()

    # Creates curves and binds them to a CurveEntry
    def create_curves(self):
        for curve in range(self.curve_limit):
            self.curve_entries[curve].setCurve(util.Curve(self.ax, self.default_verts, name="Curve " + str(curve), color=self.path_colors[curve]))

    # Function to select curve
    # updates coord entries as soon as selected, bound to CurveEntry
    def select(self, entry):
        self.curve_selected = entry
        self.change_coord_entry_values()

    def create_fig(self):
        # Making a matplotlib figure
        # self.fig = plt.figure(figsize=(5, 5))
        self.fig = plt.figure()

        self.fig.canvas.set_window_title("Curve Path Generator")
        self.ax = self.fig.add_subplot(111)
        self.ax.set_position([.1, 0, .8, 1])

        # Create image overlay
        if self.image_overlay_exists:
            self.overlay = util.Overlay(self.ax, self.image_location)
            # Draw Background image
            self.overlay.draw()

    # Changes coord entries
    def change_coord_entry_values(self):
        for y in range(len(self.text_entries)):
            for x in range(len(self.text_entries[y])):
                #print(self.curve_selected.getCurve().get_verts())
                self.text_entries[y][x].setText(str(self.curve_selected.getCurve().get_verts()[x][y]))


    def change_coord_system(self, bool):
        self.using_raw_rpappa_coords = bool

        if self.using_raw_rpappa_coords:
            self.overlay.clear()
            self.overlay.flip(origin="upper")
            # set  graph bounds to radio_selection
            self.x_bounds = (0, self.overlay.dim()[0])
            self.y_bounds = (self.overlay.dim()[1], 0)
            self.ax.set_xlim(self.x_bounds)
            self.ax.set_ylim(self.y_bounds)
        else:
            pass

        self.vis.plot()


    # Change starting pos
    def change_start(self, new_pos="Center"):
        self.overlay.clear()
        if not self.using_raw_rpappa_coords:
            # Center image according to radio_selection
            self.overlay.transpose(self.starting_positions[new_pos])
            # set  graph bounds to radio_selection
            self.x_bounds = (0 - self.starting_positions[new_pos][0],
                             self.overlay.dim()[0] - self.starting_positions[new_pos][0])
            self.y_bounds = (self.overlay.dim()[1] - self.starting_positions[new_pos][1],
                             0 - self.starting_positions[new_pos][1])
            self.ax.set_xlim(self.x_bounds)
            self.ax.set_ylim(self.y_bounds)

        elif self.using_raw_rpappa_coords:
            self.overlay.flip(origin="upper")
            # set  graph bounds to radio_selection
            self.x_bounds = (0, self.overlay.dim()[0])
            self.y_bounds = (self.overlay.dim()[1], 0)
            self.ax.set_xlim(self.x_bounds)
            self.ax.set_ylim(self.y_bounds)

        self.vis.plot()

    # Runs the gui
    def run(self):
        self.window.show()

    # Update gui, bound to update_button
    def update_gui(self):
        # cycle through entries
        for entry in self.curve_entries:


            if entry.isCurveVisible():
                entry.getCurve().draw()
            # elif not entry.isCurveVisible():
                # entry.setCurveVisible(False)

        self.vis.plot()










app = widget.QApplication(sys.argv)

curve_path_generator = CurvePathGenerator()
curve_path_generator.run()
sys.exit(app.exec_())