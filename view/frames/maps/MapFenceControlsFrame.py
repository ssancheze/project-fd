import tkintermapview
import tkinter as tk
import tkinter.ttk as ttk

from model.tkintermap import MapViewTileServers as Tiles
from view.frames.BasicFrame import BasicFrame
from controller.MapController import MapViewFrameController


class MapFenceControlsFrame(BasicFrame):
    def __init__(self, master, map_view: tkintermapview.TkinterMapView, controller: MapViewFrameController):
        super().__init__(master, no_grid=True, navigation_buttons=False, label='MAP CONTROLS')

        self.map_view = map_view
        self.controller = controller

        # POLYGON MOUSE EVENTS

        # Control variable
        self.drawing_polygon = False

        # Start polygon mouse event
        self.map_view.add_right_click_menu_command('Start Polygon Here', self.mouse_start_poly_click, pass_coords=True)
        self.map_view.add_right_click_menu_command('Close Polygon', self.mouse_close_poly_click, pass_coords=False)
        self.map_view.add_right_click_menu_command('Cancel Polygon', self.mouse_cancel_poly_click, pass_coords=False)
        self.map_view.add_left_click_map_command(self.mouse_left_click_callback)

        # Tile set dropdown
        dropdown_vals = [key for key in Tiles.__dict__ if
                         '__' not in key and '_zoom' not in key and 'method' not in key]
        self.dropdown_var = tk.StringVar(value=dropdown_vals[0])
        self.tile_set_dropdown = ttk.OptionMenu(self.frame, variable=self.dropdown_var,
                                                command=self.on_tile_set_change)
        self.tile_set_dropdown.set_menu('SELECT TILE SET', *dropdown_vals)
        self.tile_set_dropdown.pack()

        # TODO: Enable dropdown if more tiles are present
        # self.tile_set_dropdown.config(state=tk.DISABLED)

        # Inclusion / Exclusion radios
        self.poly_confirm_var = tk.BooleanVar(self.frame, value=False)

        self.poly_confirm_exclusion_radio = ttk.Radiobutton(self.frame, text='Exclusion Zone',
                                                            variable=self.poly_confirm_var, value=False)
        self.pack_widget(self.poly_confirm_exclusion_radio, 'left', 2)

        self.poly_confirm_inclusion_radio = ttk.Radiobutton(self.frame, text='Inclusion Zone',
                                                            variable=self.poly_confirm_var, value=True)
        self.pack_widget(self.poly_confirm_inclusion_radio, 'left', 2)

        # Create polygon button
        self.poly_confirm_button = ttk.Button(self.frame, text='Create Polygon',
                                              command=self.poly_confirm_button_click)
        self.pack_widget(self.poly_confirm_button, 'left', 2)

        # Delete polygon button
        self.poly_delete_button = ttk.Button(self.frame, text='Delete Polygon',
                                             command=self.poly_delete_button_click)
        self.pack_widget(self.poly_delete_button, 'left', 2)

        # Save maps button
        self.save_map_button = ttk.Button(self.frame, text='Save Map As...',
                                          command=self.save_map_button_click)
        self.pack_widget(self.save_map_button, 'right', 2)

        # Load maps button
        self.load_map_button = ttk.Button(self.frame, text='Load Map...',
                                          command=self.load_map_button_click)
        self.pack_widget(self.load_map_button, 'right', 2)

        # Clear maps button
        self.clear_map_button = ttk.Button(self.frame, text='Clear Map',
                                           command=self.clear_map_button_click)
        self.pack_widget(self.clear_map_button, 'right', 2)

    def set_tile_server(self, tile_server: str, max_zoom: int):
        self.map_view.set_tile_server(tile_server=tile_server, max_zoom=max_zoom)
        self.map_view.set_zoom(self.map_view.max_zoom)

    def draw_update(self):
        self.map_view.delete_all_marker()
        self.map_view.delete_all_path()
        self.map_view.delete_all_polygon()

        _polygon = self.controller.get_idle_polygon()
        if _polygon is not None:

            _vertices = _polygon.vertices
            _coords_list = [(ii_vertex.lat, ii_vertex.lon) for ii_vertex in _vertices]
            if not _polygon.closed:
                # If not closed, draw points and lines between
                if _vertices is not None:
                    for index, ii_vertex in enumerate(_vertices):
                        self.map_view.set_marker(ii_vertex.lat, ii_vertex.lon, text=str(index))

                    if len(_coords_list) > 1:
                        self.map_view.set_path(_coords_list)
            else:
                # If its closed, draw polygon
                self.map_view.set_polygon(_coords_list)

    def mouse_left_click_callback(self, coords):
        self.controller.polygon_add_vertex(coords)
        self.draw_update()

    def mouse_start_poly_click(self, coords):
        self.controller.start_polygon(coords)
        self.draw_update()

    def mouse_close_poly_click(self):
        self.controller.close_polygon()
        self.draw_update()

    def mouse_cancel_poly_click(self):
        self.controller.cancel_polygon()
        self.draw_update()

    def poly_confirm_button_click(self):
        self.controller.polygon_confirm(self.poly_confirm_var.get())

    def poly_delete_button_click(self):
        self.controller.polygon_delete()

    def save_map_button_click(self):
        self.controller.save_map()

    def load_map_button_click(self):
        self.controller.load_map()

    def clear_map_button_click(self):
        self.controller.clear_map()

    def on_tile_set_change(self, event=None):
        # event = selected string
        self.controller.change_tile_set(event)
        self.set_tile_server(*self.controller.get_tile_set())
