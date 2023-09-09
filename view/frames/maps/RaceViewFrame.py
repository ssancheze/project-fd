import tkinter as tk
import tkinter.ttk as ttk
from os.path import join

from view.frames.BasicFrame import BasicFrame
from view.frames.maps.MapViewFrame import MapViewFrame
from view.frames.maps.MapBasicControlFrame import MapBasicControlFrame
from view.frames.RacingRosterFrame import RacingRosterFrame
from controller.RaceController import RaceController
from definitions import ASSETS_DIR, POLYGON_EXCLUSION_KWARGS, POLYGON_INCLUSION_KWARGS


class RaceViewFrame(BasicFrame):
    def __init__(self, master, race_controller: RaceController):
        super().__init__(master, grid=(1, 2), navigation_buttons=False, label='RACE')
        self.frame.columnconfigure(0, weight=10)

        self.controller = race_controller

        # Map frame
        self.map_frame = ttk.Frame(self.frame)
        self._map_class = MapViewFrame(self.map_frame)
        self.place_in_grid(self.map_frame, (0, 0))
        self._map_class.set_control_frame(MapRaceControlFrame, self.controller)

        # Order frame
        self.roster_frame = ttk.Frame(self.frame)
        self._roster_class = RacingRosterFrame(self.roster_frame, self.controller)
        self.place_in_grid(self.roster_frame, (0, 1))
        self._roster_class.update_rows()

        self.pack_frame()

    @property
    def map_class(self):
        return self._map_class

    @property
    def roster_class(self):
        return self._roster_class


class MapRaceControlFrame(MapBasicControlFrame):
    def __init__(self, master, map_view, controller: RaceController):
        super().__init__(master, map_view)

        self.controller = controller
        self._race_manager_callback = None
        self._draw_starting_points = True

        # Ready buttons
        self.ready_racers_button = ttk.Button(self.frame, text=f'ALL RACERS READY',
                                              command=self.ready_racers_button_click)
        self.pack_widget(self.ready_racers_button, 'left', 2)

        # Assets
        self._home_marker_icon = tk.PhotoImage(file=join(ASSETS_DIR, 'home_marker_25.png'))
        self._player_icons = {}
        self._player_markers = []

    def hide_starting_points(self):
        self._draw_starting_points = False

    def draw_update(self):
        self.map_view.delete_all_polygon()
        self.map_view.delete_all_marker()
        self.map_view.delete_all_path()

        self.draw_map()
        self.draw_checkpoints()
        self.draw_starting_points()

    def racer_update(self):
        if self._draw_starting_points:
            self.erase_racers()
        else:
            self.map_view.delete_all_marker()

        self.draw_racers()

    def draw_checkpoints(self):
        _checkpoints = self.controller.get_checkpoints()

        for ii_checkpoint in _checkpoints:
            _endpoints = ii_checkpoint.endpoints
            _path_list = [jj_endpoint.tuple for jj_endpoint in _endpoints]
            self.map_view.set_path(_path_list)

    def draw_map(self):
        _map = self.controller.get_map()

        if not _map:
            return

        # Draw zones
        _inclusion_zone = _map.inclusion_zone
        if _inclusion_zone:
            self.draw_zone(_inclusion_zone)
        _exclusion_zone = _map.exclusion_zone
        if _exclusion_zone:
            self.draw_zone(_exclusion_zone)

    def draw_zone(self, zone):
        # Polygon palette
        if zone.type is True:
            _zone_kwargs = POLYGON_INCLUSION_KWARGS
        else:
            _zone_kwargs = POLYGON_EXCLUSION_KWARGS

        # Polygon coordinate list
        _zone_coordinates = zone.tuple_list

        self.map_view.set_polygon(_zone_coordinates, **_zone_kwargs)

    def draw_starting_points(self):
        # Draw starting points
        starting_points = self.controller.get_starting_positions()
        for starting_point in starting_points:
            self.map_view.set_marker(*starting_point.tuple, icon=self._home_marker_icon)

    def draw_racers(self):
        for player_number, player in self.controller.get_players().items():
            telemetry_info = self.controller.get_telemetry(player_number)
            if telemetry_info:
                self._player_icons[player_number] = tk.PhotoImage(
                    file=join(ASSETS_DIR, f'racer_marker_{player.icon_color}.png'))

                racer_marker = self.map_view.set_marker(*telemetry_info.position, icon=self._player_icons[player.id],
                                                        text=player_number)
                self._player_markers.append(racer_marker)

    def erase_racers(self):
        for marker in self._player_markers:
            marker.delete()
        self._player_markers = []

    def set_race_manager_callback(self, func):
        self._race_manager_callback = func

    def ready_racers_button_click(self):
        self._race_manager_callback()


if __name__ == '__main__':
    from view.MyTk import Window

    win = Window()
    win.config()
    foo = MapViewFrame(win, MapRaceControlFrame)
    win.mainloop()
