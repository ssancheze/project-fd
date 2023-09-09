import tkintermapview
import tkinter as tk
import tkinter.ttk as ttk

from view.frames.BasicFrame import FileDialogFrame
from view.frames.maps.MapBasicControlFrame import MapBasicControlFrame, MapFenceLoader
from controller.MapViewControllers import FenceLoaderController, FenceEditorController, FenceCheckpointController
from model.utils import FenceMap, FenceZone, Vertex
from definitions import FENCES_DIR, POLYGON_IDLE_KWARGS, POLYGON_INCLUSION_KWARGS, POLYGON_EXCLUSION_KWARGS


class MapFenceLoaderControlFrame(MapFenceLoader, MapBasicControlFrame):
    def __init__(self, master, map_view: tkintermapview.TkinterMapView):
        super().__init__(master, map_view)

        self.file_dialog = FileDialogFrame(self.frame)
        self.controller = FenceLoaderController()

        # Load maps button
        self.load_map_button = ttk.Button(self.frame, text='Load Map...',
                                          command=self.load_map_button_click)
        self.pack_widget(self.load_map_button, 'right', 2)

        # Clear maps button
        self.clear_map_button = ttk.Button(self.frame, text='Clear Map',
                                           command=self.clear_map_button_click)
        self.pack_widget(self.clear_map_button, 'right', 2)

    def draw_update(self):
        # Delete everything
        self.map_view.delete_all_marker()
        self.map_view.delete_all_polygon()

        # Then re-draw map
        self.draw_map()

    def draw_map(self):
        _map: FenceMap = self.controller.get_map()

        if not _map:
            return

        # Draw zones
        _inclusion_zone = _map.inclusion_zone
        if _inclusion_zone:
            self.draw_zone(_inclusion_zone)
        _exclusion_zone = _map.exclusion_zone
        if _exclusion_zone:
            self.draw_zone(_exclusion_zone)

        # Draw home waypoint
        _home = _map.home
        if _home:
            self.draw_home(_home)

    def draw_zone(self, zone: FenceZone):
        # Polygon palette
        if zone.type is True:
            _zone_kwargs = POLYGON_INCLUSION_KWARGS
        else:
            _zone_kwargs = POLYGON_EXCLUSION_KWARGS

        # Polygon coordinate list
        _zone_coordinates = zone.tuple_list

        self.map_view.set_polygon(_zone_coordinates, **_zone_kwargs)

    def draw_home(self, home: Vertex):
        self.map_view.set_marker(home.lat, home.lon, text='HOME')

    def load_map_button_click(self):
        self.file_dialog.ask_open_waypoints(FENCES_DIR)
        _save_path: str = self.file_dialog.open_filename
        self.controller.open_map_from_file(_save_path)
        self.draw_update()

    def clear_map_button_click(self):
        self.controller.clear_map()
        self.draw_update()


class MapFenceEditorControlFrame(MapFenceLoaderControlFrame):
    def __init__(self, master, map_view):
        super().__init__(master, map_view)

        self.controller = FenceEditorController()

        # Save maps button
        self.save_map_button = ttk.Button(self.frame, text='Save Map As...',
                                          command=self.save_map_button_click)
        self.pack_widget(self.save_map_button, 'right', 2)

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

        # Polygon edition mouse events
        self.map_view.add_right_click_menu_command('Set Home Here', self.mouse_set_home,
                                                   pass_coords=True)
        self.map_view.add_right_click_menu_command('Start Polygon Here', self.mouse_start_poly,
                                                   pass_coords=True)
        self.map_view.add_right_click_menu_command('Close Polygon', self.mouse_close_poly)
        self.map_view.add_right_click_menu_command('Cancel Polygon', self.mouse_cancel_poly)
        self.map_view.add_right_click_menu_command('Clear Inclusion Zone', self.mouse_clear_inclusion_zone)
        self.map_view.add_right_click_menu_command('Clear Exclusion Zone', self.mouse_clear_exclusion_zone)
        self.map_view.add_right_click_menu_command('Clear Home', self.mouse_clear_home)
        self.map_view.add_left_click_map_command(self.mouse_left_click_callback)

    def draw_update(self):
        # Delete everything
        self.map_view.delete_all_marker()
        self.map_view.delete_all_path()
        self.map_view.delete_all_polygon()

        # Then re-draw map and idle polygon
        self.draw_map()
        self.draw_idle_polygon()

    def draw_idle_polygon(self):
        _polygon_dict = self.controller.get_idle()

        # If no idle, draw nothing
        if _polygon_dict is None:
            return

        _polygon_vertices = _polygon_dict['vertices']

        # If empty idle, draw nothing
        if not _polygon_vertices:
            return

        _polygon_coordinates = [_vertex.tuple for _vertex in _polygon_dict['vertices']]

        # If closed, draw full polygon in idle palette
        if _polygon_dict['closed'] is True:
            self.map_view.set_polygon(_polygon_coordinates, **POLYGON_IDLE_KWARGS)
        # If not closed, draw current points
        else:
            for ii_index, ii_vertex_coordinates in enumerate(_polygon_coordinates):
                self.map_view.set_marker(ii_vertex_coordinates[0], ii_vertex_coordinates[1], text=str(ii_index))

            # If more than 1 point, draw path in between
            if len(_polygon_coordinates) > 1:
                self.map_view.set_path(_polygon_coordinates)

    def save_map_button_click(self):
        if self.controller.can_save_map():
            self.file_dialog.ask_save_waypoints(FENCES_DIR)
            self.controller.save_to_file(self.file_dialog.save_filename)

    def poly_confirm_button_click(self):
        self.controller.add_idle_to_map(self.poly_confirm_var.get())
        self.draw_update()

    def poly_delete_button_click(self):
        self.controller.clear_idle()
        self.draw_update()

    def mouse_left_click_callback(self, coords):
        self.controller.add_waypoint(coords)
        self.draw_update()

    def mouse_set_home(self, coords):
        self.controller.set_home(coords)
        self.draw_update()

    def mouse_start_poly(self, coords):
        self.controller.start_polygon(coords)
        self.draw_update()

    def mouse_close_poly(self):
        self.controller.close_polygon()
        self.draw_update()

    def mouse_cancel_poly(self):
        self.controller.cancel_polygon()
        self.draw_update()

    def mouse_clear_inclusion_zone(self):
        self.controller.clear_map_inclusion_zone()
        self.draw_update()

    def mouse_clear_exclusion_zone(self):
        self.controller.clear_map_exclusion_zone()
        self.draw_update()

    def mouse_clear_home(self):
        self.controller.clear_home()
        self.draw_update()


class MapFenceCheckpointControlFrame(MapFenceLoaderControlFrame):
    def __init__(self, master, map_view):
        super().__init__(master, map_view)

        self.controller = FenceCheckpointController()

        # Generate checkpoints button
        self.generate_div_button = ttk.Button(self.frame, text='Generate Checkpoints',
                                              command=self.generate_div_button_click)
        self.pack_widget(self.generate_div_button, 'left', 2)

        # Clear checkpoints button
        self.clear_div_button = ttk.Button(self.frame, text='Clear Checkpoints', command=self.clear_div_button_click)
        self.pack_widget(self.clear_div_button, 'left', 2)

    def draw_update(self):
        self.map_view.delete_all_polygon()
        self.map_view.delete_all_marker()
        self.map_view.delete_all_path()

        self.draw_map()
        self.draw_checkpoints()

    def draw_checkpoints(self):
        _checkpoints = self.controller.get_checkpoints()

        for ii_checkpoint in _checkpoints:
            _endpoints = ii_checkpoint.endpoints
            _path_list = [jj_endpoint.tuple for jj_endpoint in _endpoints]
            self.map_view.set_path(_path_list)

    def generate_div_button_click(self):
        self.controller.create_checkpoints()
        self.draw_update()

    def clear_div_button_click(self):
        self.controller.create_checkpoints()
        self.draw_update()


def _ready_buttons_text(id_player):
    return f'READY PLAYER {id_player}'


if __name__ == '__main__':
    import view.MyTk as MyTk
    from view.frames.maps.MapViewFrame import MapViewFrame


    def main():
        #  FENCE LOADER TESTER
        win = MyTk.Window()
        win.config()
        MapViewFrame(win, MapFenceLoaderControlFrame)
        win.mainloop()


    main()
