"""This is the configuration file which stores the program configuration parameters. It is not advised to change this
manually, as any changes to the parameters' keys will render the code unusable, be sure to only modify the values,
not the keys."""

# ____ WINDOW SETTINGS ____
# Int tuple of format (width: int, height: int)
win_windowed_resolution = (1280, 720)

# Whether the app starts in fullscreen mode or not
win_fullscreen = True

# String of value '' for none, 'h' for horizontal only, 'v' for vertical only or 'hv' / 'vh' for both.
# WARNING: may produce funky results.
win_resizable = ""

# Sets the window border
win_borderless = False


# ____ MAP SETTINGS ____
# Sets whether the map is loaded from the Internet or the local database
map_offline_mode = True
