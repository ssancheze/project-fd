import typing

import tkintermapview
import os
from definitions import MAPS_DIR

# This method creates a database with offline tiles.


def download_database(filepath: str, _server: str,
                      top_left: typing.Tuple[float, float],
                      bottom_right: typing.Tuple[float, float],
                      zoom_min: int, zoom_max: int):
    # specify the region to load (New York City)
    top_left_position = (41.2776207, 1.9806569)
    bottom_right_position = (41.2732666, 1.9906776)
    zoom_min = 17
    zoom_max = 20

    # specify path and name of the database
    _filepath_list = filepath.split('.')
    if len(_filepath_list) == 1:
        filepath += '.db'
    elif len(_filepath_list) == 2:
        if _filepath_list[1] != 'db':
            return -1
    else:
        return -1

    database_path = os.path.join(MAPS_DIR, filepath)

    # specify tile server from where tiles are downloaded
    tile_server = _server

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
    return 0
