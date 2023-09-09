"""
File containing all project constants that SHALL NOT BE MODIFIED unless you really know what you're doing.
"""
import os

# ____DIRECTORIES
# Root directory of this project
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Directory where map databases are stored
MAPS_DIR = os.path.join(ROOT_DIR, r'model\maps')

# Directory where circuit .waypoints files are stored
FENCES_DIR = os.path.join(ROOT_DIR, r'fences')

# Directory where image assets are stored
ASSETS_DIR = os.path.join(ROOT_DIR, r'assets')


# ____NAMES
# Name of this application
APPLICATION_NAME = 'ProjectFD'

# Name of the Autopilot Service
AUTOPILOT_NAME = 'AutopilotServiceMini'


# ____VALUES
# Dronlab coordinates
EETAC_COORDINATES = 41.27641629296008, 1.9886751866535248

# Maximum supported players
MAX_PLAYERS = 2

# Earth radius in meters
EARTH_RADIUS_METERS = 6371E3

# Minimum separation of a starting point from the nearest checkpoint
CHECKPOINT_SEPARATION_UNITS = 5

# Separation increment when the above is not met
CHECKPOINT_SEPARATION_INTERVAL_METERS = 0.1

# Max number of iterations for some loops
LOOP_CEILING = 10000

# Minimum distance to any checkpoint to count as crossed
CHECKPOINT_CROSSING_THRESHOLD_METERS = 2


# ____AUTOPILOT
# Mission Planner's SITL port
SITL_PORT = 5763

# Mission Planner's SITL address
SITL_ADDRESS = 'localhost'

# Mission Planner's SITL protocol
SITL_PROTOCOL = 'tcp'

# MQTT internal broker default port
MQTT_INTERNAL_PORT = 1884

# MQTT external broker default port
MQTT_EXTERNAL_PORT = 8000

# Pixhawk's autopilot default port in Raspberry Pi
RPI_PORT_ADDRESS = '/dev/ttyS0'

# Default baud rate for telemetry connection (direct mode)
TELEMETRY_BAUD = 57600

# Default baud rate for SITL and internet connection (global, local)
DEFAULT_BAUD = 115200

# Player's race heights
OPERATING_HEIGHTS = [4+(player*2) for player in range(MAX_PLAYERS)]


# ____TK
# Idle polygon palette
POLYGON_IDLE_KWARGS = {
    'fill_color': None,
    'outline_color': '#F7B801',
    'border_width': 2,
}

# Inclusion polygon palette
POLYGON_INCLUSION_KWARGS = {
    'fill_color': '#4A5859',
    'outline_color': '#F4D6CC',
    'border_width': 2,
}

# Exclusion polygon palette
POLYGON_EXCLUSION_KWARGS = {
    'fill_color': '#C83E4D',
    'outline_color': '#DD1C1A',
    'border_width': 2,
}
