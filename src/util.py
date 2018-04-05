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


# Class for Curves
class Curve():
    # Argument plot is an axis
    # Argument verts is vertices list
    # Argument Color is for curve color, defaults to black
    def __init__(self, plot, verts, color=(0, 0, 0, 1)):
        self.plot = plot
        self.verts = verts
        self.color = color
        self.codes = [1]
        for vert in range(len(self.verts) - 1):
            self.codes.append(4)
        self.path = path.Path(self.verts, self.codes)
        self.patch = patches.PathPatch(self.path, facecolor="none", lw=2)

    def draw(self):
        self.patch.set_visible(True)
        self.plot.add_patch(self.patch)

    def clear(self):
        # self.patch.remove()
        self.patch.set_visible(False)


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

    def transpose(self, transposition_coord):
        self.plot.imshow(self.img, extent=(0-transposition_coord[0], self.dim()[0] - transposition_coord[0], 0-transposition_coord[1], self.dim()[1] - transposition_coord[1]))


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

