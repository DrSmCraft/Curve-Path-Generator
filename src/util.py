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
        x = self.generate_equation_numpy()[0].deriv()
        y = self.generate_equation_numpy()[1].deriv()
        code = 'new PathSegment(t -> \n%s\n (%i * Math.pow(t, 2) + %i * t + %i) / (%i * Math.pow(t, 2) + %i * t + %i), %i)' % (self.generate_comment(), int(round(y[0])), int(round(y[1])), int(round(y[2])), int(round(x[0])), int(round(x[1])), int(round(x[2])), int(math.ceil(self.get_length())))
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

    # def generate_equation(self):
    #     # https: // javascript.info / bezier - curve
    #     x = '(1-x)**2 * %i + 2(1-x) '

    def get_length(self):
        # # https://stackoverflow.com/questions/29438398/cheap-way-of-calculating-cubic-bezier-length
        # TODO Fix this function - I don't know how to get length of a curve, right now Im averaging distance between control points
        chord = distance(self.verts[3], self.verts[0])
        cont_net = distance(self.verts[0], self.verts[1]) + distance(self.verts[1], self.verts[2]) + distance(self.verts[2], self.verts[3])
        return (cont_net + chord) / 2



    def value_at_t(self, t):
        # https://stackoverflow.com/questions/17099776/trying-to-find-length-of-a-bezier-curve-with-4-points
        # t2 = t * t;
        # t3 = t2 * t;
        # return a + (-a * 3 + t * (3 * a - a * t)) * t + (3 * b + t * (-6 * b + b * 3 * t)) * t + (c * 3 - c * 3 * t) * t2 + d * t3
        eq1 = self.generate_equation_numpy()[0](t)
        eq2 = self.generate_equation_numpy()[1](t)
        return distance((eq1, 0), (0, eq2))

    def __str__(self):
        return "Curve: " + str(self.name)

    def get_visible(self):
        return self.patch.get_visible()


# Class for Overlay
class Overlay():
    # Argument plot is an axis
    # Argument name is string containing directory name
    def __init__(self, plot, name):
        self.plot = plot
        self.name = name
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

def distance(p1, p2):
    return math.sqrt(((p2[1] - p1[1]) ** 2) + (p2[0] - p1[0]) ** 2)


# Function to get radiobutton input
def get_radio_selection(radio, option_list):
    for select in range(len(radio.circles)):
        if radio.circles[select].get_facecolor()[0] < 0.5:
            return option_list[select]

# Function to get number of a textbox
def get_number(textbox):
    try:
        out = float(textbox.text)
        return out
    except ValueError:
        return None


# Function to put text into Textbox
def put_text(textbox, text):
    #textbox.
    textbox.text = text

def write(location, text):
    with open(location, 'a+') as file:
        file.write(text + '\n\n')
        
        
# https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def check_file_exists(file):
    return os.path.exists(file)
