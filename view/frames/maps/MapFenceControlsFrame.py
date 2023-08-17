import tkintermapview
import tkinter as tk
import tkinter.ttk as ttk

from model.tkintermap import MapViewTileServers as Tiles
from view.frames.BasicFrame import BasicFrame, FileDialogFrame
from controller.MapViewController import MapViewFrameController
from definitions import FENCES_DIR


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


class MapFenceControlsFrame(BasicFrame):
    def __init__(self, master, map_view: tkintermapview.TkinterMapView, controller: MapViewFrameController):
        super().__init__(master, no_grid=True, navigation_buttons=False, label='MAP CONTROLS')

        self.map_view = map_view
        self.controller = controller
        self.file_dialog = FileDialogFrame(self.frame)

        # Control variables
        self.drawing_polygon = False

        # Start polygon mouse event
        self.map_view.add_right_click_menu_command('Set Home Here', self.mouse_set_home_click, pass_coords=True)
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
        # Delete everything
        self.map_view.delete_all_marker()
        self.map_view.delete_all_path()
        self.map_view.delete_all_polygon()

        # Then re-draw again
        self.draw_zones()
        self.draw_home()
        self.draw_idle_polygon()

    def draw_zones(self):
        _zones = self.controller.get_zones()
        if _zones:
            for ii_zone in _zones:
                _zone_coords = [(jj_vertex.lat, jj_vertex.lon) for jj_vertex in ii_zone.vertices]
                if ii_zone.type is False:
                    _zone_kwargs = POLYGON_EXCLUSION_KWARGS
                else:
                    _zone_kwargs = POLYGON_INCLUSION_KWARGS
                self.map_view.set_polygon(_zone_coords, **_zone_kwargs)

    def draw_idle_polygon(self):
        _polygon = self.controller.get_idle_polygon()

        if _polygon is not None:
            _polygon_vertices = _polygon.vertices

            if _polygon_vertices:
                if _polygon.closed:
                    # If close, draw full polygon with idle palette (kwargs)
                    _polygon_coords = [(ii_vertex.lat, ii_vertex.lon) for ii_vertex in _polygon_vertices]
                    self.map_view.set_polygon(_polygon_coords, **POLYGON_IDLE_KWARGS)

                else:
                    # If not closed, draw points and lines between
                    if _polygon_vertices is not None:
                        for index, ii_vertex in enumerate(_polygon_vertices):
                            self.map_view.set_marker(ii_vertex.lat, ii_vertex.lon, text=str(index))

                        _polygon_coords = [(ii_vertex.lat, ii_vertex.lon) for ii_vertex in _polygon_vertices]

                        if len(_polygon_coords) > 1:
                            self.map_view.set_path(_polygon_coords)

    def draw_home(self):
        _home = self.controller.get_home()
        if _home is not None:
            self.map_view.set_marker(_home.lat, _home.lon, text='HOME')

    def mouse_left_click_callback(self, coords):
        self.controller.polygon_add_vertex(coords)
        self.draw_update()

    def mouse_set_home_click(self, coords):
        self.controller.set_home(coords)
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
        self.draw_update()

    def poly_delete_button_click(self):
        self.controller.polygon_delete()
        self.draw_update()

    def save_map_button_click(self):
        if self.controller.ask_save_map():
            self.file_dialog.ask_save_waypoints(FENCES_DIR)
            self.controller.save_map(self.file_dialog.save_filename)

    def load_map_button_click(self):
        if self.controller.ask_load_map():
            self.controller.clear_map()
            self.file_dialog.ask_open_waypoints(FENCES_DIR)
            self.controller.load_map(self.file_dialog.open_filename)
            self.draw_update()

    def clear_map_button_click(self):
        self.controller.clear_map()
        self.draw_update()

    def on_tile_set_change(self, event=None):
        # event = selected string
        self.controller.change_tile_set(event)
        self.set_tile_server(*self.controller.get_tile_set())
