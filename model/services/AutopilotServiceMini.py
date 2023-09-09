from __future__ import annotations
import typing
import dronekit
import time
import threading
from math import sqrt
import paho.mqtt.client
import json

from model.services.CommunicationModeHandler import CommunicationModeHandler, MQTTClientHandler
from model.utils import Telemetry

_SERVICE_NAME = 'AutopilotServiceMini'
_TARGET_NAME = 'ProjectFD'


class AutopilotServiceMini:
    _PAYLOAD_ENCODING = 'utf-8'
    _TELEMETRY_RATE_HZ = 8
    _TELEMETRY_PERIOD = _TELEMETRY_RATE_HZ**-1

    def __init__(self, communication_mode_handler: CommunicationModeHandler, verbose=False):
        # Prints autopilot actions to the console
        self._verbose = verbose

        # Manages connection addresses
        self._communication_handler = communication_mode_handler

        # MQTT Manager init
        self._mqtt_handler = MQTTClientHandler(_SERVICE_NAME, _TARGET_NAME, self._communication_handler.drone_id)
        self._mqtt_handler.set_external_message_callback(self._on_message)
        self._mqtt_handler.connect_external(**self._communication_handler.external_broker)
        self._mqtt_handler.subscribe_external(qos=2)

        # VEHICLE ATTRIBUTES
        # Vehicle
        self._vehicle: typing.Optional[dronekit.Vehicle] = None

        # Control attributes
        self._connected: bool = False

        # Telemetry attributes
        self._sending_telemetry = False
        self._telemetry_thread: typing.Optional[threading.Thread] = None
        self._telemetry_info = Telemetry()

    def _on_message(self, message: paho.mqtt.client.MQTTMessage):
        _levels = message.topic.split('/')

        _origin_name = _levels[0]
        _destination_name = _levels[1]
        _command = _levels[-1]

        if _command == 'connect':
            self.connect()

        elif _command == 'disconnect':
            self.disconnect()

        elif _command == 'armDrone':
            self.arm()

        elif _command == 'takeOff':
            _payload = json.loads(message.payload.decode(self._PAYLOAD_ENCODING))
            _target_height = _payload['target_height']
            self.take_off(_target_height)

        elif _command == 'returnToLaunch':
            self.fast_rtl()

        elif _command == 'land':
            self.land()

        elif _command == 'altHold':
            self.altitude_hold()

        elif _command == 'stabilize':
            self.stabilize()

        elif _command == 'stop':
            self.stop()

        elif _command == 'goTo':
            _payload = json.loads(message.payload.decode(self._PAYLOAD_ENCODING))
            _lat = float(_payload['lat'])
            _lon = float(_payload['lon'])
            try:
                _height = float(_payload['height'])
            except TypeError:
                _height = bool(_payload['height'])

            self.go_to(_lat, _lon, _height)

        elif _command == 'geofenceEnable':
            self.enable_geofence()

        elif _command == 'geofenceDisable':
            self.disable_geofence()

    def connect(self, **vehicle_kwargs: typing.Dict[str, typing.Any]):
        _drone_settings = self._communication_handler.drone
        if self._verbose:
            print(f'Connecting to vehicle {self._communication_handler.drone_id} ...')
        self._vehicle = dronekit.connect(ip=_drone_settings['ip'], baud=_drone_settings['baud'],
                                         rate=self._TELEMETRY_RATE_HZ, **vehicle_kwargs)
        if self._verbose:
            print(f'Connected to vehicle {self._communication_handler.drone_id}')
        # self.disable_rc_checks()
        self._connected = True

        self.enable_telemetry()

    def enable_telemetry(self):
        self._sending_telemetry = True
        self._telemetry_thread = threading.Thread(target=self.send_telemetry_info)
        self._telemetry_thread.start()

    def disconnect(self):
        self._sending_telemetry = False
        self._telemetry_thread.join()
        self._telemetry_thread = None
        # self.reset_rc_checks()

        self._vehicle.close()
        if self._verbose:
            print(f'Disconnected from vehicle {self._communication_handler.drone_id}')
        self._connected = False
        self._mqtt_handler.publish_external('disconnectAck')

    def send_telemetry_info(self):
        while self._sending_telemetry:
            _payload = json.dumps(self.get_telemetry_info())
            self._mqtt_handler.publish_external('telemetryInfo', _payload)
            time.sleep(self._TELEMETRY_PERIOD)

    def get_telemetry_info(self):
        self._telemetry_info.set_telemetry(
            lat=self._vehicle.location.global_frame.lat,
            lon=self._vehicle.location.global_frame.lon,
            heading=self._vehicle.heading,
            groundSpeed=self._vehicle.groundspeed,
            altitude=self._vehicle.location.global_relative_frame.alt,
            battery=self._vehicle.battery.level,
            state=None
        )
        return self._telemetry_info

    def arm(self):
        # Arms vehicle and fly to aTargetAltitude
        if self._verbose:
            print('Basic Pre-Arm Checks')  # Don't try to arm until autopilot is ready
        # Copter should arm in GUIDED mode
        self._vehicle.mode = dronekit.VehicleMode('GUIDED')
        if self._verbose:
            print('Waiting For Vehicle To Initialise ...')
        while not self._vehicle.is_armable:
            time.sleep(0.5)
        if self._verbose:
            print('Arming Motors')
        self._vehicle.armed = True
        # Confirm vehicle armed before attempting to take off
        if self._verbose:
            print('Waiting For Arming ...')
        while not self._vehicle.armed:
            time.sleep(0.5)
        if self._verbose:
            print('Armed')

    def take_off(self, target_height=4):
        target_height = float(target_height)
        if self._verbose:
            print(f'Taking Off To Height: {target_height} ...')
        self._vehicle.simple_takeoff(target_height)
        while True:
            # Break and return from function just below target altitude.
            if self._vehicle.location.global_relative_frame.alt >= target_height * 0.95:
                if self._verbose:
                    print('Reached Target Height')
                break
            time.sleep(0.5)

    def rtl(self):
        if self._verbose:
            print('Returning To Launch ...')
        self._vehicle.mode = dronekit.VehicleMode('RTL')
        while self._vehicle.armed:
            time.sleep(0.5)
        if self._verbose:
            print('Landed')

    def fast_rtl(self):
        self._vehicle.mode = dronekit.VehicleMode('GUIDED')
        if self._verbose:
            print('Returning To Launch ...')
        _home = self._vehicle.home_location
        self.go_to(float(_home.lat), float(_home.lon))
        self.land()
        # self.rtl()

    def land(self):
        if self._verbose:
            print('Landing ...')
        self._vehicle.mode = dronekit.VehicleMode('LAND')
        while self._vehicle.armed:
            time.sleep(0.5)
        if self._verbose:
            print('Landed')

    def altitude_hold(self):
        self._vehicle.mode = dronekit.VehicleMode('ALT_HOLD')

    def stabilize(self):
        self._vehicle.mode = dronekit.VehicleMode('STABILIZE')

    def stop(self):
        self._vehicle.mode = dronekit.VehicleMode('BRAKE')

    def go_to(self, lat: float, lon: float, height: typing.Optional[float] = None):
        if not height:
            height = self._vehicle.location.global_relative_frame.alt
        if self._verbose:
            print(f'Going To {lat}, {lon}, height: {height} ...')
        _goto_location = dronekit.LocationGlobalRelative(lat, lon, height)
        self._vehicle.simple_goto(_goto_location)

        _current_position = self._vehicle.location.global_relative_frame
        while self.distance_meters(_current_position.lat, _current_position.lon, lat, lon) > 0.5:
            time.sleep(self._TELEMETRY_PERIOD)
            _current_position = self._vehicle.location.global_relative_frame
        if self._verbose:
            print('Point Reached')
        self._mqtt_handler.publish_external('goToReached')

    def _disable_rc_check(self):
        self._vehicle.parameters["ARMING_CHECK"] = 65470

    def _reset_rc_check(self):
        self._vehicle.parameters["ARMING_CHECK"] = 1

    def _disable_thr_fs_check(self):
        self._vehicle.parameters["FS_THR_ENABLE"] = 0

    def _reset_thr_fs_check(self):
        self._vehicle.parameters["FS_THR_ENABLE"] = 1

    def disable_rc_checks(self):
        self._disable_rc_check()
        self._disable_thr_fs_check()
        if self._verbose:
            print('RC checks disabled')

    def reset_rc_checks(self):
        self._reset_rc_check()
        self._reset_thr_fs_check()
        if self._verbose:
            print('RC checks reset')

    def enable_geofence(self):
        self._vehicle.parameters['FENCE_ENABLE'] = 1
        if self._verbose:
            print('Geofence enabled')

    def disable_geofence(self):
        self._vehicle.parameters['FENCE_ENABLE'] = 0
        if self._verbose:
            print('Geofence disabled')

    def parameter_change_acknowledge(self, parameter: str):
        _payload = json.dumps({'parameter': parameter})
        self._mqtt_handler.publish_external('parameterChanged', _payload)

    @staticmethod
    def distance_meters(lat1, lon1, lat2, lon2):
        """
        Returns the ground distance in metres between two LocationGlobal objects.

        This method is an approximation, and will not be accurate over large distances and close to the
        earth's poles. It comes from the ArduPilot test code:
        https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
        """

        lat_diff = lat2 - lat1
        lon_diff = lon2 - lon1
        return sqrt((lat_diff * lat_diff) + (lon_diff * lon_diff)) * 1.113195e5


if __name__ == '__main__':
    import dev.mqtt_debug

    def main():
        bar = CommunicationModeHandler(_SERVICE_NAME, 0)
        bar.sim_mode()
        foo = AutopilotServiceMini(bar, verbose=True)
        dev.mqtt_debug.Debugger()

    main()
