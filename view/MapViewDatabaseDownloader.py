import tkintermapview
import os
from view import MapViewTileServers as TileServers


# This scripts creates a database with offline tiles.

# specify the region to load (New York City)
top_left_position = (41.2776207, 1.9806569)
bottom_right_position = (41.2732666, 1.9906776)
zoom_min = 17
zoom_max = 20

# specify path and name of the database
file_directory = os.path.abspath(__file__)
script_directory = os.path.dirname(file_directory)+"/maps"
database_path = os.path.join(script_directory, "offline_tiles_eetac.db")

# specify tile server from where tiles are downloaded
tile_server = TileServers.gmap

# create OfflineLoader instance
loader = tkintermapview.OfflineLoader(path=database_path, tile_server=tile_server)

# save the tiles to the database, an existing database will extended
loader.save_offline_tiles(top_left_position, bottom_right_position, zoom_min, zoom_max)

# You can call save_offline_tiles() multiple times and load multiple regions into the database.
# You can also pass a tile_server argument to the OfflineLoader and specify the server to use.
# This server needs to be then also set for the TkinterMapView when the database is used.
# You can load tiles of multiple servers in the database. Which one then will be used depends on
# which server is specified for the TkinterMapView.

# print all regions that were loaded in the database
loader.print_loaded_sections()
