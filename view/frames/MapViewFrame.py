import os.path

from view.frames.BasicFrame import BasicFrame
import tkintermapview
import tkinter.ttk as ttk
import tkinter as tk
from model import MapViewTileServers as Tiles

MAP_VIEW_DATABASE_PATH = os.path.abspath('..\\maps\\offline_tiles_eetac.db')


class MapViewFrame(BasicFrame):

    def __init__(self, master=None):
        super().__init__(master, grid=(2, 1))
        self.frame.rowconfigure(0, weight=8)

        # Map view widget
        self.map_view = tkintermapview.TkinterMapView(master=self.frame, corner_radius=60, use_database_only=True)
        self.map_view.set_position(41.27641629296008, 1.9886751866535248)
        self.set_tile_server(*Tiles.method_get_tile_server('gsat'))
        self.set_db_path(os.path.join(os.getcwd(), MAP_VIEW_DATABASE_PATH))
        self.place_in_grid(self.map_view, (0, 0))

        # Map controls frame

        self.controls_frame = ttk.LabelFrame(self.frame, text='MAP CONTROLS')
        self.place_in_grid(self.controls_frame, (1, 0))

        # Tile set dropdown
        dropdown_vals = [key for key in Tiles.__dict__ if
                         '__' not in key and '_zoom' not in key and 'method' not in key]
        self.dropdown_var = tk.StringVar(value=dropdown_vals[0])
        self.tile_set_dropdown = ttk.OptionMenu(self.controls_frame, variable=self.dropdown_var,
                                                command=self.on_tile_set_change)
        self.tile_set_dropdown.set_menu('SELECT TILE SET', *dropdown_vals)
        self.tile_set_dropdown.pack()

        # Offline mode checkbutton
        # TODO: Add offline mode option in config.py and load map accordingly
        self.offline_checkbutton_var = tk.BooleanVar(value=False)
        self.offline_checkbutton = ttk.Checkbutton(self.controls_frame, text='Offline',
                                                   variable=self.offline_checkbutton_var,
                                                   command=self.on_offline_checkbutton_change)

        # Inclusion / Exclusion radios
        self.poly_confirm_var = tk.BooleanVar(self.controls_frame, value=False)

        self.poly_confirm_exclusion_radio = ttk.Radiobutton(self.controls_frame, text='Exclusion zone',
                                                            variable=self.poly_confirm_var, value=False)
        self.pack_widget(self.poly_confirm_exclusion_radio, 'left', 2)

        self.poly_confirm_inclusion_radio = ttk.Radiobutton(self.controls_frame, text='Inclusion zone',
                                                            variable=self.poly_confirm_var, value=True)
        self.pack_widget(self.poly_confirm_inclusion_radio, 'left', 2)

        # Create polygon button
        self.poly_confirm_button = ttk.Button(self.controls_frame, text='Create polygon',
                                              command=self.poly_confirm_button_click)
        self.pack_widget(self.poly_confirm_button, 'left', 2)

        self.pack_frame()

        # Delete polygon button
        self.poly_delete_button = ttk.Button(self.controls_frame, text='Delete polygon',
                                             command=self.poly_delete_button_click)
        self.pack_widget(self.poly_delete_button, 'left', 2)

        # Save map button
        self.save_map_button = ttk.Button(self.controls_frame, text='Save map',
                                          command=self.save_map_button_click)
        self.pack_widget(self.save_map_button, 'right', 2)

        # Load map button
        self.load_map_button = ttk.Button(self.controls_frame, text='Load map',
                                          command=self.load_map_button_click)
        self.pack_widget(self.load_map_button, 'right', 2)

        # Clear map button
        self.clear_map_button = ttk.Button(self.controls_frame, text='Clear map',
                                           command=self.clear_map_button_click)
        self.pack_widget(self.clear_map_button, 'right', 2)

    def poly_confirm_button_click(self):
        pass

    def poly_delete_button_click(self):
        pass

    def save_map_button_click(self):
        pass

    def load_map_button_click(self):
        pass

    def clear_map_button_click(self):
        pass

    def on_tile_set_change(self, event=None):
        set_tile_args = Tiles.method_get_tile_server(self.dropdown_var.get())
        self.set_tile_server(*set_tile_args)

    def on_offline_checkbutton_change(self, event=None):
        self.use_database(self.offline_checkbutton_var.get())

    # TEST METHODS, SHOULD BE IN MODEL dir
    def set_tile_server(self, tile_server: str, max_zoom: int):
        self.map_view.set_tile_server(tile_server=tile_server, max_zoom=max_zoom)
        self.map_view.set_zoom(self.map_view.max_zoom)

    def use_database(self, value=None):
        if value is not None:
            if isinstance(value, bool):
                self.map_view.use_database_only = value
        else:
            return self.map_view.use_database_only

    def set_db_path(self, _path: str):
        self.map_view.database_path = _path


if __name__ == '__main__':
    from view import MyTk

    def main():
        win = MyTk.Window()
        win.config()
        y = win.tk.geometry()
        MapViewFrame(win)
        win.mainloop()

    main()
