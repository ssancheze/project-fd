

class CommsManager:
    def __init__(self):
        self._communication_mode = None

        self._broker_address = None
        self._broker_username = None
        self._broker_password = None

    @property
    def communication_mode(self):
        return self._communication_mode

    @property
    def broker_address(self):
        return self._broker_address

    @property
    def broker_username(self):
        return self._broker_username

    @property
    def broker_password(self):
        return self._broker_password

    def global_mode(self, address: str, username: str = None, password: str = None):
        self._communication_mode = 'global'
        self._broker_address = address
        self._broker_username = username
        self._broker_password = password

    def local_single_mode(self):
        self._communication_mode = 'local_single'

    def local_onboard_mode(self):
        self._communication_mode = 'local_onboard'

    def direct_mode(self):
        self._communication_mode = 'direct'

    def simulation_mode(self):
        self._communication_mode = 'simulation'
