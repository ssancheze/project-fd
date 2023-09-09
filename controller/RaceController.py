from controller.MapViewControllers import FenceCheckpointController
from model.managers.PlayerManager import PlayerManager
from model.managers.TrackManager import TrackManager
from model.managers.FlightManager import FlightManager


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

    def get_position(self, player_number: int):
        pass

    def get_starting_positions(self):
        positions = [seeker.starting_point for _, seeker in self._flight_manager.seekers.items()]
        return positions

    def get_telemetry(self, player_number: int):
        return self._flight_manager.get_telemetry(player_number)


if __name__ == '__main__':
    pass
