"""
Name: main.py
Author: Sam O
Date: 3/31/18

Info:
Main run file for this app




"""


# Imports
import matplotlib.widgets as widget
import matplotlib.pyplot as plt


import util

starting_positions = {"Center": [90, 162], "Right": [90, 216], "Left": [90, 80]}

# Functions
def update(event):
    starting_radio_selection = util.get_radio_selection(starting_radio, starting_option_list)
    alliance_radio_selection = util.get_radio_selection(alliance_radio, alliance_option_list)


    # Center image according to radio_selction
    overlay.transpose(starting_positions[starting_radio_selection])
    
    # set  graph bounds to radio_selection
    x_bounds = (0 - starting_positions[starting_radio_selection][0], overlay.dim()[0] - starting_positions[starting_radio_selection][0])
    y_bounds = (0 - starting_positions[starting_radio_selection][1], overlay.dim()[1] - starting_positions[starting_radio_selection][1])
    ax.set_xlim(x_bounds)
    ax.set_ylim(y_bounds)

    # get vals from textboxes
    try:
        verts[0] = (util.get_number(startx), util.get_number(starty))
        verts[1] = (util.get_number(endx), util.get_number(endy))
    except:
        verts.append((util.get_number(endx), util.get_number(endy)))

    curve = util.Curve(ax, verts)
    curve.draw()


# Colors
RED = (1, 0, 0, 1)
BLUE = (0, 0, 1, 1)
YELLOW = (1, 1, 0, 1)
BLACK = (0, 0, 0, 1)



verts = [(0, 0)]
curves = []



fig = plt.figure()
ax = fig.add_subplot(111)

# Starting Radio
ax_starting_radio = plt.axes([0.0, 0.5, 0.1, .1])
starting_option_list = ["Left", "Center", "Right"]
starting_radio = widget.RadioButtons(ax_starting_radio, starting_option_list)

# Alliance Radio
ax_alliance_radio = plt.axes([0.0, 0.7, 0.1, 0.1])
alliance_option_list = ["Red", "Blue"]
alliance_radio = widget.RadioButtons(ax_alliance_radio, alliance_option_list)

# Update Button
ax_update_button = plt.axes([0.0, 0.0, 0.1, 0.1])
text = "Update"
update_button = widget.Button(ax_update_button, text)
update_button.on_clicked(update)
overlay = util.Overlay(ax, "overlay.png")

# Text Inputs
startx_ax = plt.axes([.2, .1, .05, .05])
starty_ax = plt.axes([.3, .1, .05, .05])
endx_ax = plt.axes([.2, 0, .05, .05])
endy_ax = plt.axes([.3, 0, .05, .05])
mid1x_ax = plt.axes([.6, .1, .05, .05])
mid1y_ax = plt.axes([.7, .1, .05, .05])
mid2x_ax = plt.axes([.6, 0, .05, .05])
mid2y_ax = plt.axes([.7, 0, .05, .05])

startx = widget.TextBox(startx_ax, "Start X", initial="0")
starty = widget.TextBox(starty_ax, "Start Y", initial="0")
endx = widget.TextBox(endx_ax, "End X", initial="0")
endy = widget.TextBox(endy_ax, "End Y", initial="0")
mid1x = widget.TextBox(mid1x_ax, "Mid1 X", initial="0")
mid1y = widget.TextBox(mid1y_ax, "Mid1 Y", initial="0")
mid2x = widget.TextBox(mid2x_ax, "Mid2 X", initial="0")
mid2y = widget.TextBox(mid2y_ax, "Mid2 Y", initial="0")


# startx.on_submit(util.submit_number)
# starty.on_submit(util.submit_number)
# endx.on_submit(util.submit_number)
# endy.on_submit(util.submit_number)
# mid1x.on_submit(util.submit_number)
# mid1y.on_submit(util.submit_number)
# mid2x.on_submit(util.submit_number)
# mid2y.on_submit(util.submit_number)

overlay.draw()

#Graph Bounds
x_bounds = (0, overlay.dim()[0])
y_bounds = (0, overlay.dim()[1])

xs, ys = zip(*verts)


ax.set_xlim(x_bounds)
ax.set_ylim(y_bounds)



plt.show()

