import tkintermapview
import tkinter as tk
import tkinter.ttk as ttk
from abc import ABC

from view.frames.BasicFrame import BasicFrame
import model.maps.MapViewTileServers as Tiles


class MapBasicControlFrame(BasicFrame):
    def __init__(self, master, map_view: tkintermapview.TkinterMapView):
        """
        Basic control frame for the MapView. Used to change between map tile sets.
        :param master: tk parent frame/window
        :param map_view: the tkintermapview widget
        """
        BasicFrame.__init__(self, master, no_grid=True, navigation_buttons=False, label='MAP CONTROLS')

        self.map_view = map_view
        self.controller = None

        # Tile set dropdown
        dropdown_vals = Tiles.map_tiles_dict()
        self.dropdown_var = tk.StringVar(value=dropdown_vals[0])
        self.tile_set_dropdown = ttk.OptionMenu(self.frame, variable=self.dropdown_var,
                                                command=self.on_tile_set_change)
        self.tile_set_dropdown.set_menu('SELECT TILE SET', *dropdown_vals)
        self.tile_set_dropdown.pack()

    def on_tile_set_change(self, event=None):
        # event = selected string
        _tile_server, _max_zoom = Tiles.get_tile_server(event)
        self.map_view.set_tile_server(tile_server=_tile_server, max_zoom=_max_zoom)
        self.map_view.set_zoom(self.map_view.max_zoom)


class MapFenceLoader(ABC):
    pass

    def draw_update(self):
        pass

    def draw_map(self):
        pass

    def draw_zone(self, zone):
        pass

    def draw_home(self, home):
        pass

    def load_map_button_click(self):
        pass

    def clear_map_button_click(self):
        pass
