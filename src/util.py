"""
Name:
Author:
Date:

Info:




"""


# Imports
import matplotlib.path as path
import matplotlib.patches as patches
import matplotlib.image as m_image
import PIL.Image as image


class Curve():
    def __init__(self, plot, verts):
        self.plot = plot
        self.verts = verts
        self.codes = [1]
        for vert in range(len(self.verts) - 1):
            self.codes.append(4)
        self.path = path.Path(self.verts, self.codes)
        self.patch = patches.PathPatch(self.path, facecolor="none", lw=2)



    def draw(self):
        self.plot.add_patch(self.patch)

class Overlay():
    def __init__(self, plot, name):
        self.plot = plot
        self.name = name
        self.im = image.open(self.name, "r")

    def draw(self):
        self.img = m_image.imread(self.name)
        self.plot.imshow(self.img)

    def dim(self):
        return [self.im.width, self.im.height]

    def transpose(self, transpose_coord):
        #self.img.
        self.plot.imshow(self.im, origin="upper")

class Line():
    def __init__(self, plot, start, end, color, thickness):
        self.plot = plot
        self.start = start
        self.end = end
        self.color = color
        self.thickness = thickness
        self.line = patches.Rectangle(self.start, (self.end[0] - self.start[0]) + thickness[0], (self.end[1] - self.start[1]) + thickness[1])
        self.line.set_color(self.color)

    def draw(self):
        self.plot.add_patch(self.line)


def get_radio_selection(radio, option_list):
    for select in range(len(radio.circles)):
        if radio.circles[select].get_facecolor()[0] < 0.5:
            return option_list[select]


