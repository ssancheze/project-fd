import typing

from model.PlayerManager import PlayerManager
from model.TrackManager import TrackManager
from model.FlightManager import FlightManager
from controller.RaceController import RaceController


class RaceManager:
    def __init__(self, player_manager: PlayerManager, track_manager: TrackManager, flight_manager: FlightManager):
        self._player_manager: PlayerManager = player_manager
        self._track_manager: TrackManager = track_manager
        self._flight_manager: FlightManager = flight_manager

        self._race_controller: RaceController = RaceController(self._player_manager,
                                                               self._track_manager,
                                                               self._flight_manager)

    @property
    def race_controller(self):
        return self._race_controller


if __name__ == '__main__':
    pass
