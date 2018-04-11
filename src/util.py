"""
Name: util.py
Author: Sam O
Date: 3/31/18

Info:
File for useful classes and functions.

"""

# Imports
import matplotlib.path as path
import matplotlib.patches as patches
import matplotlib.image as m_image
import PIL.Image as image
import numpy as np
import math
import os
import sys
import PyQt5.QtWidgets as widget

# Class for Curves
class Curve():
    # Argument plot is an axis
    # Argument verts is vertices list
    # Argument Color is for curve color, defaults to black
    def __init__(self, plot, verts, color=(0, 0, 0, 1), name="Curve"):
        self.plot = plot
        self.verts = verts
        self.color = color
        self.name = name
        self.codes = [1]
        for vert in range(len(self.verts) - 1):
            self.codes.append(4)
        self.path = path.Path(self.verts, self.codes)
        self.patch = patches.PathPatch(self.path, facecolor="none", lw=2)
        self.patch.fill = False
        self.patch.set_color(self.color)

        self.equation = self.generate_equation()

    def draw(self):
        self.patch.set_visible(True)
        self.plot.add_patch(self.patch)

    def clear(self):
        # self.patch.remove()
        self.patch.set_visible(False)

    def generate_comment(self):
        string = '/*{"start":{"x":%i, "y":%i}, "mid1":{"x":%i, "y":%i}, "mid2":{"x":%i, "y":%i}, "end":{"x":%i, "y":%i}} */' % (self.verts[0][0], self.verts[0][1], self.verts[1][0], self.verts[1][1], self.verts[2][0], self.verts[2][1], self.verts[3][0], self.verts[3][1])
        return string

    def generate_code(self):
        # new
        # PathSegment(t ->
        # / *{"start": {"x": 100, "y": 25}, "mid1": {"x": 10, "y": 90}, "mid2": {"x": 110, "y": 100},
        #     "end": {"x": 150, "y": 195}} * /
        #    (195 + -330 * t + 420 * Math.pow(t, 2)) / (-270 + 1140 * t + -750 * Math.pow(t, 2))
        # , 214)
        x = self.equation[0].deriv()
        y = self.equation[1].deriv()
        code = 'new PathSegment(t -> \n%s\n (%i * Math.pow(t, 2) + %i * t + %i) / (%i * Math.pow(t, 2) + %i * t + %i), %i)' % (self.generate_comment(), int(round(y[2])), int(round(y[1])), int(round(y[0])), int(round(x[2])), int(round(x[1])), int(round(x[0])), int(math.ceil(self.get_length())))
        return code

    def generate_equation_numpy(self):
        # Finding equation
        xlist, ylist = zip(*self.verts)
        tt = np.linspace(0, 5, len(xlist))
        x_param = np.polyfit(tt, xlist, 3)
        y_param = np.polyfit(tt, ylist, 3)
        eq_x = np.poly1d(x_param)
        eq_y = np.poly1d(y_param)
        return [eq_x, eq_y]

    def generate_equation(self):
        # https: // javascript.info / bezier - curve
        # http://mathfaculty.fullerton.edu/mathews/n2003/BezierCurveMod.html
        x0, y0 = self.verts[0]
        x1, y1 = self.verts[1]
        x2, y2 = self.verts[2]
        x3, y3 = self.verts[3]

        # Finding x
        term3_x = (x3 - x0 + (3 * x1) - (3 * x2))
        term2_x = (3 * (x0 + x2 - (2 * x1)))
        term1_x = (3 * (x1 - x0))
        term0_x = x0
        eq_x = np.poly1d([term3_x, term2_x, term1_x, term0_x])

        # Finding y
        term3_y = (y3 - y0 + (3 * y1) - (3 * y2))
        term2_y = (3 * (y0 + y2 - (2 * y1)))
        term1_y = (3 * (y1 - y0))
        term0_y = y0
        eq_y = np.poly1d([term3_y, term2_y, term1_y, term0_y])

        return [eq_x, eq_y]


    def get_length(self):
        total = 0
        previous = self.verts[0]
        for t in range(0, 100):
            if self.value_at_t(t)[0] >= self.verts[3][0] or self.value_at_t(t)[1] >= self.verts[3][1]:
                return total
            total += distance(self.value_at_t(t), previous)
            previous = self.value_at_t(t)
        return total

    def value_at_t(self, t):
        eq1 = self.generate_equation_numpy()[0]
        eq2 = self.generate_equation_numpy()[1]
        return [eq1(t), eq2(t)]

    def __str__(self):
        return "Curve: " + str(self.name)

    def get_visible(self):
        return self.patch.get_visible()


# Class for Overlay
class Overlay():
    # Argument plot is an axis
    # Argument name is string containing directory name
    def __init__(self, plot, name, alliance="Red"):
        self.plot = plot
        self.name = name
        self.alliance = alliance
        self.im = image.open(self.name, "r")
        self.img = m_image.imread(self.name)

    def draw(self):
        self.plot.imshow(self.img)

    def dim(self):
        return [self.im.width, self.im.height]

    def transpose(self, transposition_coord, origin='lower'):
        self.plot.set_visible(False)
        self.plot.imshow(self.img, origin=origin, extent=(0-transposition_coord[0], self.dim()[0] - transposition_coord[0], 0-transposition_coord[1], self.dim()[1] - transposition_coord[1]))
        self.plot.set_visible(True)

    def flip(self, origin="lower"):
        self.transpose([0, 0], origin=origin)

    def invert(self):
        self.img = np.fliplr(self.img)

    def flip_alliance(self, alliance="Red"):
        if alliance == "Blue":
            if self.alliance == "Red":
                self.alliance = "Blue"
                self.invert()

        elif alliance == "Red":
            if self.alliance == "Blue":
                self.alliance = "Red"
                self.invert()
        else:
            print("Alliance code is wrong")
            pass


# https://stackoverflow.com/questions/12459811/how-to-embed-matplotlib-in-pyqt-for-dummies#12465861
class M_Canvas(widget.QDialog):
    def __init__(self, parent=None, figure=None):
        super(M_Canvas, self.win).__init__()
        self.win.parent = parent
        self.win.figure = figure


def distance(p1, p2):
    return math.sqrt(((p2[1] - p1[1]) ** 2) + (p2[0] - p1[0]) ** 2)

#def derivative(equation):

# Function to get radiobutton input
def get_radio_selection(radio, option_list):
    for select in range(len(radio.circles)):
        if radio.circles[select].get_facecolor()[0] < 0.5:
            return option_list[select]


# Function to get number of a textbox ---> Matplotlib
def get_number(textbox):
    try:
        out = float(textbox.text)
        return out
    except ValueError:
        return None


# Function to put text into Textbox ---> Matplotlib
def put_text(textbox, text):
    textbox.text = text


def write(location, text):
    with open(location, 'a+') as file:
        file.write(text + '\n\n')


def run_script(file):
    os.system(file)


def exit():
    sys.exit()


def check_file_exists(file):
    return os.path.exists(file)
