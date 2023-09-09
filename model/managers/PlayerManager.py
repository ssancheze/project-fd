from typing import Dict, Union, List

from model.utils import Racer, Stopwatch, Tracker, Telemetry, Checkpoint
from model.managers.CommsManager import CommsManager
from model.services.CommunicationModeHandler import CommunicationModeHandler
from definitions import APPLICATION_NAME


class PlayerManager:
    def __init__(self, communications_manager: CommsManager):
        self._players: Dict[int, Racer] = {}

        self._communications_manager: CommsManager = communications_manager
        self._communication_handlers: Dict[int, CommunicationModeHandler] = {}
        self._stopwatches: Dict[int, Stopwatch] = {}
        self._trackers: Dict[int, Tracker] = {}

    def link_stopwatch(self, player_number: int):
        self._stopwatches[player_number] = Stopwatch()

        self.players[player_number].set_stopwatch(
            self._stopwatches[player_number]
        )

    def link_tracker(self, player_number: int, telemetry_info: Telemetry, checkpoints: List[Checkpoint],
                     zone_lengths: List[float]):
        self._trackers[player_number] = Tracker(telemetry_info, checkpoints, zone_lengths)

        self.players[player_number].set_tracker(
            self._trackers[player_number]
        )

    @property
    def players(self):
        return self._players

    @property
    def players_list(self) -> List[Racer]:
        return [racer for _, racer in self._players.items()]

    @property
    def communication_handlers(self):
        return self._communication_handlers

    @property
    def trackers(self):
        return self._trackers

    def add_player(self, racer_number: int, icon_color: str):
        self._players[racer_number] = Racer(racer_number, icon_color)

    def link_communication_handler(self, racer_number: int, address: Union[str, int, None] = None):
        racer_communication_handler = CommunicationModeHandler(APPLICATION_NAME, racer_number)

        mode = self._communications_manager.communication_mode
        if mode == 'global':
            racer_communication_handler.global_mode(address)
        elif mode == 'local_single':
            racer_communication_handler.local_single_mode('localhost')
        elif mode == 'local_onboard':
            racer_communication_handler.local_onboard_mode(address)
        elif mode == 'direct':
            racer_communication_handler.direct_mode(int(address))
        elif mode == 'simulation':
            racer_communication_handler.sim_mode()

        self._communication_handlers[racer_number] = racer_communication_handler
        self._players[racer_number].set_communication_handler(self._communication_handlers[racer_number])
