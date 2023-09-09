from __future__ import annotations

import typing

from paho.mqtt import client as mqtt

from definitions import (RPI_PORT_ADDRESS, SITL_ADDRESS, SITL_PROTOCOL, SITL_PORT, TELEMETRY_BAUD, DEFAULT_BAUD,
                         MQTT_EXTERNAL_PORT, MQTT_INTERNAL_PORT)


class CommunicationModeHandler:
    _ADDRESS_DICT = {
        'AutopilotServiceMini': {
            'global': {
                'external_address': None,
                'internal_address': 'localhost',
                'drone_address': RPI_PORT_ADDRESS,
                'drone_baud': DEFAULT_BAUD
            },

            'local_single': {
                'external_address': None,
                'internal_address': 'localhost',
                'drone_address': RPI_PORT_ADDRESS,
                'drone_baud': DEFAULT_BAUD
            },

            'local_onboard': {
                'external_address': 'localhost',
                'internal_address': 'localhost',
                'drone_address': RPI_PORT_ADDRESS,
                'drone_baud': DEFAULT_BAUD
            },

            'direct': {
                'external_address': None,
                'internal_address': 'localhost',
                'drone_address': None,
                'drone_baud': TELEMETRY_BAUD
            },

            'simulation': {
                'external_address': 'localhost',
                'internal_address': 'localhost',
                'drone_address': f'{SITL_PROTOCOL}:{SITL_ADDRESS}:{SITL_PORT}',
                'drone_baud': DEFAULT_BAUD
            }
        },

        'ProjectFD': {
            'global': {
                'external_address': None,
            },

            'local_single': {
                'external_address': 'localhost',
            },

            'local_onboard': {
                'external_address': None,
            },

            'direct': {
                'external_address': 'localhost',
            },

            'simulation': {
                'external_address': 'localhost'
            }
        }
    }

    def __init__(self, service_name: str, drone_id: int):
        """
        Handles the broker and drone communication parameters from the DEE communication modes.
        """
        # Service name
        self._service_name = service_name

        # Drone id
        self._drone_id = drone_id

        # Communication mode: 'global', 'local_single', 'local_onboard' or 'direct'
        self._communication_mode: typing.Optional[str] = None

        # Copy of the _ADDRESS_DICT with custom settings
        self._communication_dict = CommunicationModeHandler._ADDRESS_DICT.copy()

        # External broker credentials
        self._external_broker_username: typing.Optional[str] = None
        self._external_broker_password: typing.Optional[str] = None

    @property
    def communication_mode(self):
        return self._communication_mode

    def global_mode(self, external_broker_address: str,
                    external_broker_username: typing.Optional[str] = None,
                    external_broker_password: typing.Optional[str] = None):
        self._communication_mode = 'global'
        self._external_broker_username = external_broker_username
        self._external_broker_password = external_broker_password
        self._set_param('external_address', external_broker_address)

    def local_onboard_mode(self, drone_ip_address: str):
        self._communication_mode = 'local_onboard'
        self._set_param('external_address', drone_ip_address)

    def local_single_mode(self, gcs_ip_address: str):
        self._communication_mode = 'local_single'
        self._set_param('external_address', gcs_ip_address)

    def direct_mode(self, telemetry_radio_com_port: int):
        self._communication_mode = 'direct'
        self._set_param('drone_address', f'COM{telemetry_radio_com_port}')

    def sim_mode(self):
        self._communication_mode = 'simulation'

    def _get_settings(self) -> dict:
        return self._communication_dict[self._service_name][self._communication_mode]

    def _set_param(self, param: str, value: typing.Union[str, int]):
        self._communication_dict[self._service_name][self._communication_mode][param] = value

    @property
    def external_broker(self):
        _settings = self._get_settings()
        return {
            'host': _settings['external_address'],
            'port': MQTT_EXTERNAL_PORT
        }

    @property
    def external_broker_credentials(self):
        return {
            'username': self._external_broker_username,
            'password': self._external_broker_password
        }

    @property
    def internal_broker(self):
        _settings = self._get_settings()
        return {
            'host': _settings['external_address'],
            'port': MQTT_INTERNAL_PORT
        }

    @property
    def drone(self):
        _settings = self._get_settings()
        return {
            'ip': _settings['drone_address'],
            'baud': _settings['drone_baud']
        }

    @property
    def drone_id(self):
        return self._drone_id


class MQTTClientHandler:
    def __init__(self, origin_service_name: str, destination_service_name: str, drone_id: int):
        """
        Sets up an mqtt link between two applications
        :param origin_service_name: name of the origin service
        :param destination_service_name: name of the destination service
        :param drone_id: id of the communicating drone
        """
        # Drone id
        self._drone_id = drone_id

        # Origin and destination names for message publishing
        self._origin_name = origin_service_name
        self._destination_name = destination_service_name

        # Internal broker, unused
        self._internal_broker = MQTTClient(self._origin_name+'_internal')

        # External broker
        self._external_broker = MQTTClient(self._origin_name+'_external', transport='websockets')

    def connect_external(self, host, port: int):
        self._external_broker.connect(host, port)

    def subscribe_external(self, qos=0):
        _topic = f'{self._destination_name}/{self._origin_name}/{str(self._drone_id)}/#'
        self._external_broker.subscribe(_topic, qos)

    def publish_external(self, command: str, payload=None):
        _topic = f'{self._origin_name}/{self._destination_name}/{str(self._drone_id)}/{command}'
        self._external_broker.publish(_topic, payload)

    def connect_internal(self, host: str, port: int):
        self._internal_broker.connect(host, port)

    def subscribe_internal(self, qos=0):
        # Every drone has its internal broker so no id used
        _topic = f'{self._destination_name}/{self._origin_name}/#'
        self._internal_broker.subscribe(_topic, qos)

    def publish_internal(self, command, payload=None):
        # Every drone has its internal broker so no id used
        _topic = f'{self._origin_name}/{self._destination_name}/{command}'
        self._internal_broker.publish(_topic, payload)

    def disconnect(self):
        self._internal_broker.disconnect()
        self._external_broker.disconnect()

    def set_external_message_callback(self, func: typing.Callable):
        """
        Sets the function to be executed when a message from the external broker is received
        :param func: a function that takes exactly one argument: message
        """
        self._external_broker.set_message_callback(func)


class MQTTClient:
    def __init__(self, client_id: str, transport: str = 'tcp'):
        self._client: typing.Optional[mqtt.Client] = None
        self._client_id = client_id
        self._transport = transport
        self._message_callback: typing.Optional[typing.Callable] = None

    def connect(self, host, port):
        if not self._client:
            self._client = mqtt.Client(client_id=self._client_id, transport=self._transport)
            self._client.on_message = self._message_callback
            self._client.connect(host=host, port=port)
            self._client.loop_start()

    def disconnect(self):
        if self._client:
            self._client.disconnect()
            self._client = None

    def set_message_callback(self, func: typing.Callable):
        def _message_callback(client, userdata, message):
            func(message)

        self._message_callback = _message_callback

    def publish(self, topic, payload, qos=0):
        if self._client:
            self._client.publish(topic, payload, qos)

    def subscribe(self, topic, qos=0):
        if self._client:
            self._client.subscribe(topic, qos)


if __name__ == '__main__':
    foo = CommunicationModeHandler('AutopilotServiceMini', 0)
    foo2 = CommunicationModeHandler('AutopilotServiceMini', 1)
