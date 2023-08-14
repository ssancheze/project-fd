"""This file contains the addresses of the map tile servers used by the module tkintermapview. The maximum zoom level
for the map may also be needed depending on the scaling of the tiles."""
default_zoom = 19

osm = "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png"
osm_max_zoom = default_zoom

gmap = "https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga"
gmap_max_zoom = 20

gsat = "https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga"
gsat_max_zoom = 20


#  METHODS
def method_get_tile_server(tile_server: str):
    max_zoom = globals()[f'{tile_server}_max_zoom']
    tile_server = globals()[f'{tile_server}']
    return tile_server, max_zoom
