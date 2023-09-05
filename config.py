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

# Hide window borders
win_borderless = False


# ____ MAP SETTINGS ____
# Load the map using a database in model\maps\
map_offline_mode = True


# ____ RACE SETTINGS ____
# Displays circuit checkpoints
race_show_checkpoints = False


# ____ AUTOPILOT SETTINGS ____
