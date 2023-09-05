"""This file contains the addresses of the map tile servers used by the module tkintermapview. The maximum zoom level
for the map may also be needed depending on the scaling of the tiles."""
default_zoom = 19

osm_address = "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png"
osm_max_zoom = default_zoom

gmap_address = "https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga"
gmap_max_zoom = 20

gsat_address = "https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga"
gsat_max_zoom = 20


#  METHODS
def get_tile_server(tile_server: str):
    max_zoom = globals()[f'{tile_server}_max_zoom']
    tile_server = globals()[f'{tile_server}_address']
    return tile_server, max_zoom


def map_tiles_dict():
    return [_key.strip('_address') for _key in globals().keys() if 'address' in _key]


if __name__ == '__main__':
    print(map_tiles_dict())
