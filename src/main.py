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


# Update figure
# Called when Update Button is pressed
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

    # Get Values from Textboxes and put them into verts
    verts = []
    verts.append((util.get_number(startx), util.get_number(starty)))
    verts.append((util.get_number(mid1x), util.get_number(mid1y)))
    verts.append((util.get_number(mid2x), util.get_number(mid2y)))
    verts.append((util.get_number(endx), util.get_number(endy)))

    # Create Curve
    curve = util.Curve(ax, verts)
    curve.draw()
    print(curve.generate_code())


# Vertice list
verts = [(0, 0),
         (50, 0),
         (0, 50),
         (100, 50)]


# Making a matplotlib fugure
fig = plt.figure()
ax = fig.add_subplot(111)

# Starting Radio Button
ax_starting_radio = plt.axes([0.0, 0.5, 0.1, .1])
starting_option_list = ["Left", "Center", "Right"]
starting_radio = widget.RadioButtons(ax_starting_radio, starting_option_list)

# Alliance Radio Buttons
ax_alliance_radio = plt.axes([0.0, 0.7, 0.1, 0.1])
alliance_option_list = ["Red", "Blue"]
alliance_radio = widget.RadioButtons(ax_alliance_radio, alliance_option_list)

# Update Button
ax_update_button = plt.axes([0.0, 0.0, 0.1, 0.1])
text = "Update"
update_button = widget.Button(ax_update_button, text)
update_button.on_clicked(update)
overlay = util.Overlay(ax, 'C:\\Users\\Notebook\\Desktop\\Curve Path Generator\\src\\overlay.png')

# Text Inputs
startx_ax = plt.axes([.2, .1, .05, .05])
starty_ax = plt.axes([.3, .1, .05, .05])
endx_ax = plt.axes([.2, 0, .05, .05])
endy_ax = plt.axes([.3, 0, .05, .05])
mid1x_ax = plt.axes([.6, .1, .05, .05])
mid1y_ax = plt.axes([.7, .1, .05, .05])
mid2x_ax = plt.axes([.6, 0, .05, .05])
mid2y_ax = plt.axes([.7, 0, .05, .05])

startx = widget.TextBox(startx_ax, "Start X", initial=str(verts[0][0]))
starty = widget.TextBox(starty_ax, "Start Y", initial=str(verts[0][1]))
mid1x = widget.TextBox(mid1x_ax, "Mid1 X", initial=str(verts[1][0]))
mid1y = widget.TextBox(mid1y_ax, "Mid1 Y", initial=str(verts[1][1]))
mid2x = widget.TextBox(mid2x_ax, "Mid2 X", initial=str(verts[2][0]))
mid2y = widget.TextBox(mid2y_ax, "Mid2 Y", initial=str(verts[2][1]))
endx = widget.TextBox(endx_ax, "End X", initial=str(verts[3][0]))
endy = widget.TextBox(endy_ax, "End Y", initial=str(verts[3][1]))

# Draw Background image
overlay.draw()

# Set graph bound to 0 --> overlay size
x_bounds = (0, overlay.dim()[0])
y_bounds = (0, overlay.dim()[1])

# Set graph bounds
ax.set_xlim(x_bounds)
ax.set_ylim(y_bounds)

# Show graph
plt.show()

