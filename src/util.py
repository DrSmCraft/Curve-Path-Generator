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
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.image as m_image
import PIL.Image as image
import numpy as np
import math
import os
import sys
import PyQt5.QtWidgets as widget
import PyQt5.QtGui as gui

# Class for Curves
class Curve():
    # Argument plot is an axis
    # Argument verts is vertices list
    # Argument Color is for curve color, defaults to black
    def __init__(self, plot, verts, color=(0, 0, 0, 1), name="Curve", control_points=True):
        self.plot = plot
        self.control_points = control_points
        self.verts = verts
        self.color = color
        self.name = name
        self.codes = [1]
        for vert in range(len(self.verts) - 1):
            self.codes.append(4)
        self.path = path.Path(self.verts, self.codes)
        self.patch = patches.PathPatch(self.path, facecolor="none", lw=2)
        self.points = None
        self.patch.fill = False
        self.patch.set_color(self.color)



        self.equation = self.generate_equation()
        self.start_angle = self.get_start_angle()
        self.end_angle = self.get_end_angle()
        #print("Start angle: " + str(self.start_angle), "End angle: " + str(self.end_angle))

    def draw(self):
        self.patch.set_visible(True)
        self.plot.add_patch(self.patch)
        if self.control_points:
            self.anchors = self.plot.plot(*zip(*self.verts), marker='o', ls='')

    def clear(self):
        self.patch.set_visible(False)
        self.anchors.pop(0).remove()

    def set_visable(self, bool):
        # TODO Figure this out
        self.patch.set_visible(bool)
        self.anchors.pop(0).remove()


    def generate_comment(self):
        string = '/*{"start":{"x":%i, "y":%i}, "mid1":{"x":%i, "y":%i}, "mid2":{"x":%i, "y":%i}, "end":{"x":%i, "y":%i}, "startAngle":%d, "endAngle":%d} */' % (self.verts[0][0], self.verts[0][1], self.verts[1][0], self.verts[1][1], self.verts[2][0], self.verts[2][1], self.verts[3][0], self.verts[3][1], self.start_angle, self.end_angle)
        return string

    def generate_code(self):
        x = self.equation[0].deriv()
        y = self.equation[1].deriv()
        code = 'new PathSegment(t -> \n%s\n (%i * Math.pow(t, 2) + %i * t + %i) / (%i * Math.pow(t, 2) + %i * t + %i), %i)' % (self.generate_comment(), int(round(y[2])), int(round(y[1])), int(round(y[0])), int(round(x[2])), int(round(x[1])), int(round(x[0])), int(math.ceil(self.get_length())))
        return code

    def generate_equation(self):
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
        # total = 0
        # previous = self.verts[0]
        # for t in range(0, 100, 1):
        #     if self.value_at_t(t)[0] >= self.verts[3][0] or self.value_at_t(t)[1] >= self.verts[3][1]:
        #         return total
        #     total += distance(self.value_at_t(t/100), previous)
        #     previous = self.value_at_t(t/100)
        # return total
        chord = distance(self.verts[0], self.verts[3])
        sum = distance(self.verts[0], self.verts[1]) + distance(self.verts[1], self.verts[2]) + distance(self.verts[2], self.verts[3])
        return (chord + sum) / 2

    def get_end_angle(self):
        eq = get_linear_equation(self.verts[2], self.verts[3])
        return math.degrees(get_angle(np.poly1d([0, 0]), eq))

    def get_start_angle(self):
        eq = get_linear_equation(self.verts[0], self.verts[1])
        return math.degrees(get_angle(np.poly1d([0, 0]), eq))

    def value_at_t(self, t):
        eq1 = self.equation[0]
        eq2 = self.equation[1]
        return [eq1(t), eq2(t)]

    def __str__(self):
        return "Curve: " + str(self.name)

    def get_visible(self):
        return self.patch.get_visible()

    def set_visible(self, new_state):
        self.patch.set_visible(new_state)

    def change_start(self, new_coord):
        self.verts[0] = new_coord

    def change_mid1(self, new_coord):
        self.verts[1] = new_coord

    def change_mid2(self, new_coord):
        self.verts[2] = new_coord

    def change_end(self, new_coord):
        self.verts[3] = new_coord

    def change_verts(self, new_verts):
        self.verts = new_verts

    def get_verts(self):
        return self.verts


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











def make_points_from_string(comment_string=None, equation_string=None):
    def make_points_from_comment(string):
        out = []
        for i in string.split("{"):
            if i[1] == "x":
                comma_index = i.index(",")
                end_semicolon = i.index("}", comma_index)
                out.append([int(i[4:comma_index]), int(i[comma_index + 6: end_semicolon])])
            print(i)

        return out

    if comment_string is not None and equation_string is not None:
        return make_points_from_comment(comment_string)




# Returns distince between two points
def distance(p1, p2):
    return math.sqrt(((p2[1] - p1[1]) ** 2) + (p2[0] - p1[0]) ** 2)


# Returns polynomial equation of tangent line to equation at x
def tangent_line(equation, x):
    y = equation(x)
    slope = equation.deriv()(x)
    b = y - (slope * x)
    eq = [slope, b]
    return np.poly1d(eq)


# Returns angle between two linear polynomials (in radians)
def get_angle(eq1, eq2):
    a1 = math.atan(eq1[1])
    a2 = math.atan(eq2[1])
    return math.pi - abs(a1 - a2)


# get linear equation given two points
def get_linear_equation(point1, point2):
    x1, y1 = point1[0], point1[1]
    x2, y2 = point2[0], point2[1]
    try:
        slope = (y2 - y1) / (x2 - x1)
    except ZeroDivisionError:
        slope = 0
    b = y1 - (slope * x1)
    eq = [slope, b]
    return np.poly1d(eq)



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
