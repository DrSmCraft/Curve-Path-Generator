"""
Name: main.py
Author: Sam O
Date: 3/31/18

Info:
Main run file for this app

App based on Team 340 path generator
Located here ---> http://paths.rpappa.com/
Github ---> https://github.com/greater-rochester-robotics
"""


# Imports
import matplotlib.widgets as widget
import matplotlib.pyplot as plt

import util

# TODO Change GUI to PyQt5
# https://stackoverflow.com/questions/12459811/how-to-embed-matplotlib-in-pyqt-for-dummies


# Main Class
class CurvePathGenerator():
    def __init__(self):
        self.starting_positions = {"Center": [90, 162],
                                    "Left": [90, 216],
                                    "Right": [90, 80]}
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
                              (0, 50),
                              (100, 50)]
        self.using_raw_rpappa_coords = True
        self.image_overlay_exists = False

        # Path to image
        self.image_location = 'overlay.png'
        self.image_overlay_exists = util.check_file_exists(self.image_location)

        # Path to output file
        self.text_location = 'code.txt'

        # Curves List
        self.curves = []

        # Reset the Graph
        self.set(None)

    def set(self, event):
        # Making a matplotlib figure
        self.fig = plt.figure()
        self.fig.canvas.set_window_title("Curve Path Generator")
        self.ax = self.fig.add_subplot(111)


        # Starting Radio Button
        ax_starting_radio = plt.axes([0.0, 0.5, 0.1, .1])
        self.starting_option_list = ["Right", "Center", "Left"]
        self.starting_radio = widget.RadioButtons(ax_starting_radio, self.starting_option_list)

        # Alliance Radio Buttons
        ax_alliance_radio = plt.axes([0.0, 0.7, 0.1, 0.1])
        self.alliance_option_list = ["Red", "Blue"]
        self.alliance_radio = widget.RadioButtons(ax_alliance_radio, self.alliance_option_list)

        # Coord system radio button
        ax_coord_system = plt.axes([0.8, 0.8, 0.2, 0.1])
        self.coord_system_option_list = ["Native Coord System", "Rpappa Coord System"]
        self.coord_system_radio = widget.RadioButtons(ax_coord_system, self.coord_system_option_list)

        # Update Button
        ax_update_button = plt.axes([0.0, 0.0, 0.1, 0.1])
        update_text = "Update"
        self.update_button = widget.Button(ax_update_button, update_text)
        self.update_button.on_clicked(self.update)

        # Create image overlay
        if self.image_overlay_exists:
            self.overlay = util.Overlay(self.ax, self.image_location)
            # Draw Background image
            self.overlay.draw()

        # Reset Button
        # ax_reset_button = plt.axes([0.9, 0.0, 0.1, 0.1])
        # reset_text = "Reset"
        # self.reset_button = widget.Button(ax_reset_button, reset_text)
        # self.reset_button.on_clicked(self.reset)

        # Text Inputs
        startx_ax = plt.axes([.2, .1, .05, .05])
        starty_ax = plt.axes([.35, .1, .05, .05])
        endx_ax = plt.axes([.2, 0, .05, .05])
        endy_ax = plt.axes([.35, 0, .05, .05])
        mid1x_ax = plt.axes([.6, .1, .05, .05])
        mid1y_ax = plt.axes([.75, .1, .05, .05])
        mid2x_ax = plt.axes([.6, 0, .05, .05])
        mid2y_ax = plt.axes([.75, 0, .05, .05])

        self.startx = widget.TextBox(startx_ax, "Start X", initial=str(self.default_verts[0][0]))
        self.starty = widget.TextBox(starty_ax, "Start Y", initial=str(self.default_verts[0][1]))
        self.mid1x = widget.TextBox(mid1x_ax, "Mid1 X", initial=str(self.default_verts[1][0]))
        self.mid1y = widget.TextBox(mid1y_ax, "Mid1 Y", initial=str(self.default_verts[1][1]))
        self.mid2x = widget.TextBox(mid2x_ax, "Mid2 X", initial=str(self.default_verts[2][0]))
        self.mid2y = widget.TextBox(mid2y_ax, "Mid2 Y", initial=str(self.default_verts[2][1]))
        self.endx = widget.TextBox(endx_ax, "End X", initial=str(self.default_verts[3][0]))
        self.endy = widget.TextBox(endy_ax, "End Y", initial=str(self.default_verts[3][1]))

        if self.image_overlay_exists:
            # Set graph bound to 0 --> overlay size
            self.x_bounds = (0, self.overlay.dim()[0])
            self.y_bounds = (0, self.overlay.dim()[1])
        else:
            # Set graph bound to 0 --> (2000, 1000)
            print("Overlay Image not Found!")
            self.x_bounds = (0, 1000)
            self.y_bounds = (0, 1000)

        # Set graph bounds
        self.ax.set_xlim(self.x_bounds)
        self.ax.set_ylim(self.y_bounds)

    def reset(self, event):
        util.run_script("main.exe")
        util.exit()

    # Update figure
    # Called when Update Button is pressed
    def update(self, event):
        if self.image_overlay_exists:
            self.color_path_count += 1
            starting_radio_selection = util.get_radio_selection(self.starting_radio, self.starting_option_list)
            alliance_radio_selection = util.get_radio_selection(self.alliance_radio, self.alliance_option_list)

            # Switch overlay orientation based on alliance_radio_selection
            self.overlay.flip_alliance(alliance=alliance_radio_selection)


            # Check if using rpappa coords
            if util.get_radio_selection(self.coord_system_radio, self.coord_system_option_list) == self.coord_system_option_list[0]:
                self.using_raw_rpappa_coords = False
            elif util.get_radio_selection(self.coord_system_radio, self.coord_system_option_list) == self.coord_system_option_list[1]:
                self.using_raw_rpappa_coords = True

            if not self.using_raw_rpappa_coords:
                # Center image according to radio_selection
                self.overlay.transpose(self.starting_positions[starting_radio_selection])

                # set  graph bounds to radio_selection
                self.x_bounds = (0 - self.starting_positions[starting_radio_selection][0],
                        self.overlay.dim()[0] - self.starting_positions[starting_radio_selection][0])
                self.y_bounds = (0 - self.starting_positions[starting_radio_selection][1],
                        self.overlay.dim()[1] - self.starting_positions[starting_radio_selection][1])
                self.ax.set_xlim(self.x_bounds)
                self.ax.set_ylim(self.y_bounds)
            elif self.using_raw_rpappa_coords:
                self.overlay.flip(origin="upper")
                # set  graph bounds to radio_selection
                self.x_bounds = (0, self.overlay.dim()[0])
                self.y_bounds = (self.overlay.dim()[1], 0)
                self.ax.set_xlim(self.x_bounds)
                self.ax.set_ylim(self.y_bounds)

            # Get Values from Textboxes and put them into verts
            verts = []
            verts.append((util.get_number(self.startx), util.get_number(self.starty)))
            verts.append((util.get_number(self.mid1x), util.get_number(self.mid1y)))
            verts.append((util.get_number(self.mid2x), util.get_number(self.mid2y)))
            verts.append((util.get_number(self.endx), util.get_number(self.endy)))

            # Create Curve
            curve = util.Curve(self.ax, verts, color=self.path_colors[self.color_path_count % 10])
            self.curves.append(curve)
            index = self.curves.index(curve)
            if self.curves[index - 1] is not None:
                self.curves[index - 1].clear()

            self.curves[index].draw()
            for text in self.fig.texts:
                text.remove()
            util.write(self.text_location, curve.generate_code())
            self.fig.text(0, .9, curve.generate_code())
            print(curve.generate_code())
        else:
            print("Overlay Image not Found!")

    def show(self):
        # Show the Graph
        plt.show()


if __name__ == "__main__":
    app = CurvePathGenerator()
    app.show()









