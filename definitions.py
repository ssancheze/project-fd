import os
"""

"""

# ____DIRECTORIES
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

MAPS_DIR = os.path.join(ROOT_DIR, r'model\maps')

FENCES_DIR = os.path.join(ROOT_DIR, r'fences')

ASSETS_DIR = os.path.join(ROOT_DIR, r'assets')


# ____VALUES
EETAC_COORDINATES = 41.27641629296008, 1.9886751866535248

MAX_RACERS = 2

EARTH_RADIUS_METERS = 6371E3

CHECKPOINT_SEPARATION_UNITS = 5

CHECKPOINT_SEPARATION_INTERVAL_METERS = 0.1

TELEMETRY_RATE_HZ = 8

LOOP_CEILING = 10000


# ____AUTOPILOT
SITL_PORT = 5763

SITL_ADDRESS = 'localhost'

SITL_PROTOCOL = 'tcp'

MQTT_INTERNAL_PORT = 1884

MQTT_EXTERNAL_PORT = 8000

RPI_PORT_ADDRESS = '/dev/ttyS0'

TELEMETRY_BAUD = 57600

DEFAULT_BAUD = 115200

# ____TK
POLYGON_IDLE_KWARGS = {
    'fill_color': None,
    'outline_color': '#F7B801',
    'border_width': 2,

}

POLYGON_INCLUSION_KWARGS = {
    'fill_color': '#4A5859',
    'outline_color': '#F4D6CC',
    'border_width': 2,

}

POLYGON_EXCLUSION_KWARGS = {
    'fill_color': '#C83E4D',
    'outline_color': '#DD1C1A',
    'border_width': 2,

}
