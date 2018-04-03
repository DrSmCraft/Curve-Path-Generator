"""
Name:
Author:
Date:

Info:




"""


# Imports
import matplotlib.widgets as widget
import matplotlib.pyplot as plt


import util

starting_positions = {"Center":[90, 162], "Right":[90, 216], "Left":[90, 80]}

# Functions
def update(event):
    starting_radio_selection = util.get_radio_selection(starting_radio, starting_option_list)
    alliance_radio_selection = util.get_radio_selection(alliance_radio, alliance_option_list)
    print("jjj")
    #TODO Center image according to radio_selction
    overlay.transpose([0, 0])
    
    #TODO set  graph bounds to radio_selection
    x_bounds = (0 - starting_positions[starting_radio_selection][0], overlay.dim()[0] - starting_positions[starting_radio_selection][0])
    y_bounds = (0 - starting_positions[starting_radio_selection][1], overlay.dim()[1] - starting_positions[starting_radio_selection][1])
    ax.set_xlim(x_bounds)
    ax.set_ylim(y_bounds)





# Colors
RED = (1, 0, 0, 1)
BLUE = (0, 0, 1, 1)
YELLOW = (1, 1, 0, 1)
BLACK = (0, 0, 0, 1)



verts = [
    (0, 0),
    (100, 100),
    (80, 200),
    (8, 0)]




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
curve = util.Curve(ax, verts)
overlay = util.Overlay(ax, "overlay.png")

curve.draw()
overlay.draw()

#Graph Bounds
x_bounds = (0, overlay.dim()[0])
y_bounds = (0, overlay.dim()[1])

xs, ys = zip(*verts)


ax.set_xlim(x_bounds)
ax.set_ylim(y_bounds)



plt.show()

