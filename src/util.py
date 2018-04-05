"""
Name: util.py
Author: Sam O
Date: 3/31/18

Info:
File for useful classes and functions.



"""

print("Util loading")

# Imports
import matplotlib.path as path
import matplotlib.patches as patches
import matplotlib.image as m_image
import PIL.Image as image
import matplotlib.widgets as widget
import numpy as np
import scipy.misc as misc

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
        self.img = m_image.imread(self.name)


    def draw(self):
        self.plot.imshow(self.img)

    def dim(self):
        return [self.im.width, self.im.height]

    def transpose(self, transposition_coord):
        self.plot.imshow(self.img, extent=(0-transposition_coord[0], self.dim()[0] - transposition_coord[0], 0-transposition_coord[1], self.dim()[1] - transposition_coord[1]))

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

def submit_number(text):
    try:
        out = float(text)
        return text
    except:
        return None


def get_number(textbox):
    try:
        out = float(textbox.text)
        return out
    except:
        return None


# def bernstein_poly(i, n, t):
#     """
#      The Bernstein polynomial of n, i as a function of t
#     """
#
#     return misc.comb(n, i) * ( t**(n-i) ) * (1 - t)**i
#
#
# def bezier_curve(points, nTimes=1000):
#     """
#        Given a set of control points, return the
#        bezier curve defined by the control points.
#
#        points should be a list of lists, or list of tuples
#        such as [ [1,1],
#                  [2,3],
#                  [4,5], ..[Xn, Yn] ]
#         nTimes is the number of time steps, defaults to 1000
#
#         See http://processingjs.nihongoresources.com/bezierinfo/
#     """
#
#     nPoints = len(points)
#     xPoints = np.array([p[0] for p in points])
#     yPoints = np.array([p[1] for p in points])
#
#     t = np.linspace(0.0, 1.0, nTimes)
#
#     polynomial_array = np.array([ bernstein_poly(i, nPoints-1, t) for i in range(0, nPoints)   ])
#
#     xvals = np.dot(xPoints, polynomial_array)
#     yvals = np.dot(yPoints, polynomial_array)
#
#     return xvals, yvals

#print(bezier_curve([(0, 0), (100, 0), (50, 50)]))
#print(type(print(quadBrezPoints((0, 0), (100, 0), (50, 50), 5))))
print("Util loaded")