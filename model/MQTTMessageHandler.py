import typing
import json
import paho.mqtt.client

from model.CommunicationModeHandler import CommunicationModeHandler, MQTTClientHandler
from model.RaceClasses import Telemetry


_TARGET_NAME = 'AutopilotServiceMini'
_SERVICE_NAME = 'ProjectFD'


class AutopilotServiceController:
    _PAYLOAD_ENCODING = 'utf-8'

    def __init__(self, communication_handler: CommunicationModeHandler, drone_id: int):
        self._communication_handler = communication_handler
        self._drone_id = drone_id

        self._mqtt_handler = MQTTClientHandler(_SERVICE_NAME, _TARGET_NAME, self._drone_id)
        self._mqtt_handler.set_external_message_callback(self._on_message)
        self._mqtt_handler.connect_external(**self._communication_handler.external_broker)
        self._mqtt_handler.subscribe_external()

        self._telemetry_info: Telemetry = Telemetry()
        self._telemetry_callback: typing.List[typing.Callable] = []

        self._parameter_change_waiting_ack: bool = False
        self._waiting_go_to: bool = False

    @property
    def telemetry_info(self):
        return self._telemetry_info

    @property
    def drone_id(self):
        return self._drone_id

    @property
    def waiting_parameter_change_ack(self):
        return self._parameter_change_waiting_ack

    @property
    def waiting_go_to(self):
        return self._waiting_go_to

    def vehicle_connect(self):
        self._mqtt_handler.publish_external('connect')

    def vehicle_disconnect(self):
        self._mqtt_handler.publish_external('disconnect')

    def vehicle_arm(self):
        self._mqtt_handler.publish_external('armDrone')

    def vehicle_take_off(self, target_height: float):
        _payload = {'target_height': target_height}
        self._mqtt_handler.publish_external('takeOff', json.dumps(_payload))

    def vehicle_go_to(self, lat: float, lon: float, height: typing.Optional[float] = None):
        _payload = {'lat': lat, 'lon': lon, 'height': height}
        self._mqtt_handler.publish_external('goTo', json.dumps(_payload))
        self._waiting_go_to = True

    def vehicle_rtl(self):
        self._mqtt_handler.publish_external('returnToLaunch')

    def vehicle_stop(self):
        self._mqtt_handler.publish_external('stop')

    def vehicle_altitude_hold(self):
        self._mqtt_handler.publish_external('altHold')

    def vehicle_geofence_enable(self):
        self._mqtt_handler.publish_external('geofenceEnable')
        self._parameter_change_waiting_ack = True

    def vehicle_geofence_disable(self):
        self._mqtt_handler.publish_external('geofenceDisable')
        self._parameter_change_waiting_ack = True

    def _on_message(self, message: paho.mqtt.client.MQTTMessage):
        _levels = message.topic.split('/')

        _origin_name = _levels[0]
        _destination_name = _levels[1]
        _command = _levels[-1]

        if _command == 'telemetryInfo':
            _payload = json.loads(message.payload.decode(self._PAYLOAD_ENCODING))
            self.update_telemetry(_payload)

        elif _command == 'parameterChanged':
            self._parameter_change_waiting_ack = False

        elif _command == 'goToReached':
            self._waiting_go_to = False

    def update_telemetry(self, telemetry_dict: dict):
        self._telemetry_info.set_telemetry(**telemetry_dict)
        for _func in self._telemetry_callback:
            _func()

    def register_telemetry_callback(self, func: typing.Callable):
        self._telemetry_callback.append(func)

    def disconnect_handler(self):
        self._mqtt_handler.disconnect()


if __name__ == '__main__':
    pass
