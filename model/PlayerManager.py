from typing import Dict, Union, List

from dev.utils import Racer
from model.CommsManager import CommsManager
from model.CommunicationModeHandler import CommunicationModeHandler
from definitions import APPLICATION_NAME


class PlayerManager:
    def __init__(self, communications_manager: CommsManager):
        self._players: Dict[int, Racer] = {}

        self._communications_manager: CommsManager = communications_manager
        self._communication_handlers: Dict[int, CommunicationModeHandler] = {}

    @property
    def players(self):
        return self._players

    @property
    def players_list(self) -> List[Racer]:
        return [racer for _, racer in self._players.items()]

    @property
    def communication_handlers(self):
        return self._communication_handlers

    def add_player(self, racer_number: int):
        self._players[racer_number] = Racer(racer_number)

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
