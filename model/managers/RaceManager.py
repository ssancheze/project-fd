from typing import Optional
from time import sleep

from model.managers.PlayerManager import PlayerManager
from model.managers.TrackManager import TrackManager
from model.managers.FlightManager import FlightManager
from controller.RaceController import RaceController
from view.frames.maps.RaceViewFrame import RaceViewFrame


class RaceManager:
    def __init__(self, player_manager: PlayerManager, track_manager: TrackManager, flight_manager: FlightManager):
        self._player_manager: PlayerManager = player_manager
        self._track_manager: TrackManager = track_manager
        self._flight_manager: FlightManager = flight_manager

        self._race_controller: RaceController = RaceController(self._player_manager,
                                                               self._track_manager,
                                                               self._flight_manager)
        self._race_view: Optional[RaceViewFrame] = None

    @property
    def race_controller(self):
        return self._race_controller

    def start_race_sequence(self):
        print('STARTING RACE, PLEASE HOLD...')
        for player_number in self._player_manager.players:
            self._flight_manager.seek_start_point(player_number, callback=self.continue_race_sequence)

    def continue_race_sequence(self):
        print('3...')
        sleep(1)
        print('2...')
        sleep(1)
        print('1...')
        sleep(1)
        print('GO!')
        self._race_view.map_class.control_frame.hide_starting_points()
        for player_number in self._player_manager.players:
            self._flight_manager.bind_telemetry(player_number, self._player_manager.trackers[player_number].track)

    def bind_race_view(self, race_view: RaceViewFrame):
        self._race_view = race_view
        self._race_view.map_class.control_frame.set_race_manager_callback(self.start_race_sequence)


if __name__ == '__main__':
    pass
