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
        self.map_view = tkintermapview.TkinterMapView(master=self.frame, corner_radius=60)
        # FIXME: Remove position placeholder
        self.map_view.set_position(41.27641629296008, 1.9886751866535248)
        # self.set_db_path(os.path.join(os.getcwd(), MAP_VIEW_DATABASE_PATH))
        self.place_in_grid(self.map_view, (0, 0))

        # Map controls frame
        self.controls_frame = MapControlsFrame(self.frame, self.map_view)
        self.controls_frame.set_tile_server(*Tiles.method_get_tile_server('gsat'))
        self.place_in_grid(self.controls_frame.frame, (1, 0))

        # End
        self.pack_frame()


class MapControlsFrame(BasicFrame):
    def __init__(self, master, map_view: tkintermapview.TkinterMapView):
        super().__init__(master, no_grid=True, navigation_buttons=False, label='MAP CONTROLS')

        self.map_view = map_view

        # Tile set dropdown
        dropdown_vals = [key for key in Tiles.__dict__ if
                         '__' not in key and '_zoom' not in key and 'method' not in key]
        self.dropdown_var = tk.StringVar(value=dropdown_vals[0])
        self.tile_set_dropdown = ttk.OptionMenu(self.frame, variable=self.dropdown_var,
                                                command=self.on_tile_set_change)
        self.tile_set_dropdown.set_menu('SELECT TILE SET', *dropdown_vals)
        self.tile_set_dropdown.pack()

        # TODO: Add offline mode option in config.py and load map accordingly

        # Inclusion / Exclusion radios
        self.poly_confirm_var = tk.BooleanVar(self.frame, value=False)

        self.poly_confirm_exclusion_radio = ttk.Radiobutton(self.frame, text='Exclusion zone',
                                                            variable=self.poly_confirm_var, value=False)
        self.pack_widget(self.poly_confirm_exclusion_radio, 'left', 2)

        self.poly_confirm_inclusion_radio = ttk.Radiobutton(self.frame, text='Inclusion zone',
                                                            variable=self.poly_confirm_var, value=True)
        self.pack_widget(self.poly_confirm_inclusion_radio, 'left', 2)

        # Create polygon button
        self.poly_confirm_button = ttk.Button(self.frame, text='Create polygon',
                                              command=self.poly_confirm_button_click)
        self.pack_widget(self.poly_confirm_button, 'left', 2)

        # Delete polygon button
        self.poly_delete_button = ttk.Button(self.frame, text='Delete polygon',
                                             command=self.poly_delete_button_click)
        self.pack_widget(self.poly_delete_button, 'left', 2)

        # Save map button
        self.save_map_button = ttk.Button(self.frame, text='Save map',
                                          command=self.save_map_button_click)
        self.pack_widget(self.save_map_button, 'right', 2)

        # Load map button
        self.load_map_button = ttk.Button(self.frame, text='Load map',
                                          command=self.load_map_button_click)
        self.pack_widget(self.load_map_button, 'right', 2)

        # Clear map button
        self.clear_map_button = ttk.Button(self.frame, text='Clear map',
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

    # TEST METHODS, SHOULD BE IN MODEL dir
    def set_tile_server(self, tile_server: str, max_zoom: int):
        self.map_view.set_tile_server(tile_server=tile_server, max_zoom=max_zoom)
        self.map_view.set_zoom(self.map_view.max_zoom)


if __name__ == '__main__':
    from view import MyTk

    def main():
        win = MyTk.Window()
        win.config()
        y = win.tk.geometry()
        MapViewFrame(win)
        win.mainloop()

    main()
