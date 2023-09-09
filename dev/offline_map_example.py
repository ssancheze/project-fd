"""
Simple window that loads a tkintermapview from an offline database stored in MAPS_DIR (model/maps/*)
"""
import tkinter
import os
from tkintermapview import TkinterMapView
from model.maps import MapViewTileServers as Tiles
from definitions import MAPS_DIR

# create tkinter window
top_left_position = (41.2776207, 1.9806569)
bottom_right_position = (41.2732666, 1.9906776)
root_tk = tkinter.Tk()
root_tk.geometry(f"{1000}x{700}")
root_tk.title("map_view_simple_example.py")

# path for the database to use
database_path = os.path.join(MAPS_DIR, "offline_tiles_eetac_gsat.db")

# create maps widget and only use the tiles from the database, not the online server (use_database_only=True)
map_widget = TkinterMapView(root_tk, width=1000, height=700, corner_radius=0, use_database_only=True,
                            max_zoom=20, database_path=database_path)
map_widget.set_position(41.27641629296008, 1.9886751866535248)
map_widget.tile_server = Tiles.gsat_address
map_widget.min_zoom = 20
map_widget.set_zoom(20)


# map_widget.fit_bounding_box(top_left_position, bottom_right_position)

map_widget.pack(fill="both", expand=True)

root_tk.mainloop()
