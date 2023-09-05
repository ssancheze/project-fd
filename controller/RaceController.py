from controller.MapViewControllers import FenceCheckpointController
from model.PlayerManager import PlayerManager
from model.TrackManager import TrackManager
from model.FlightManager import FlightManager


class RaceController(FenceCheckpointController):
    def __init__(self, player_manager: PlayerManager, track_manager: TrackManager, flight_manager: FlightManager):
        """
        Controller for the RaceViewerFrame.
        """
        super().__init__()

        self._player_manager = player_manager
        self._track_manager = track_manager
        self._flight_manager = flight_manager

        self._model = self._track_manager.race_model

    def get_players(self):
        return self._player_manager.players

    def get_players_list(self):
        return self._player_manager.players_list

    def set_all_ready(self):
        for racer in self._player_manager.players_list:
            racer.set_ready()

    def get_position(self, player_number: int):
        pass


if __name__ == '__main__':
    pass
