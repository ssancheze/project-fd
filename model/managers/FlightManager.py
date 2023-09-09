from typing import Dict, Callable

from model.managers.PlayerManager import PlayerManager
from model.managers.TrackManager import TrackManager
from model.services.MQTTMessageHandler import AutopilotServiceController
from model.utils import Seeker, Vertex
from definitions import OPERATING_HEIGHTS


class FlightManager:
    def __init__(self, player_manager: PlayerManager, track_manager: TrackManager):
        self._player_manager: PlayerManager = player_manager

        self._track_manager: TrackManager = track_manager

        self._autopilot_controllers: Dict[int, AutopilotServiceController] = {}
        self._operating_heights: Dict[int, float] = {}
        self._operating_heights_list = OPERATING_HEIGHTS.copy()
        self._seekers: Dict[int, Seeker] = {}

    @property
    def seekers(self):
        return self._seekers

    @property
    def autopilot_controllers(self):
        return self._autopilot_controllers

    def link_autopilot_controller(self, player_number: int):
        self._autopilot_controllers[player_number] = AutopilotServiceController(
            self._player_manager.communication_handlers[player_number], player_number
        )
        self._player_manager.players[player_number].set_autopilot_controller(
            self._autopilot_controllers[player_number]
        )

    def link_seeker(self, player_number: int, starting_point: Vertex, starting_zone_absolute: int):
        self._operating_heights[player_number] = self._operating_heights_list.pop()

        self._seekers[player_number] = Seeker(starting_point, starting_zone_absolute,
                                              self._autopilot_controllers[player_number],
                                              self._operating_heights[player_number])

        self._player_manager.players[player_number].set_seeker(self._seekers[player_number])

    def seek_start_point(self, player_number: int, callback):
        return self._seekers[player_number].t_seek_starting_point(callback)
        # self._seekers[player_number].seek_starting_point()

    def bind_telemetries(self, callback: Callable):
        for player_number in self._autopilot_controllers:
            self.bind_telemetry(player_number, callback)

    def connect_players(self):
        for _, instance in self._autopilot_controllers.items():
            instance.vehicle_connect()

    def bind_telemetry(self, player_number: int, callback: Callable):
        self._autopilot_controllers[player_number].register_telemetry_callback(callback)

    def get_telemetry(self, player_number: int):
        return self._autopilot_controllers[player_number].telemetry_info


if __name__ == '__main__':
    pass
