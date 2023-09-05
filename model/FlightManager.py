from typing import Optional, Dict

from model.PlayerManager import PlayerManager
from model.TrackManager import TrackManager
from model.MQTTMessageHandler import AutopilotServiceController
from dev.utils import Stopwatch, Tracker


class FlightManager:
    def __init__(self, player_manager: PlayerManager, track_manager: TrackManager):
        self._player_manager: PlayerManager = player_manager

        self._track_manager: TrackManager = track_manager

        self._autopilot_controllers: Dict[int, AutopilotServiceController] = {}
        self._stopwatches: Dict[int, Stopwatch] = {}
        self._trackers: Dict[int, Tracker] = {}

    def link_autopilot_controller(self, player_number: int):
        self._autopilot_controllers[player_number] = AutopilotServiceController(
            self._player_manager.communication_handlers[player_number], player_number
        )
        self._player_manager.players[player_number].set_autopilot_controller(
            self._autopilot_controllers[player_number]
        )

    def link_stopwatch(self, player_number: int):
        self._stopwatches[player_number] = Stopwatch()

        self._player_manager.players[player_number].set_stopwatch(
            self._stopwatches[player_number]
        )

    def link_tracker(self, player_number: int):
        self._trackers[player_number] = Tracker()

        self._player_manager.players[player_number].set_tracker(
            self._trackers[player_number]
        )


if __name__ == '__main__':
    pass
