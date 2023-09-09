from __future__ import annotations

import time
import typing
from math import radians, sin, cos, asin, sqrt
from typing import Optional, List, Tuple
from datetime import timedelta
from time import time, sleep
from threading import Thread

from definitions import (EARTH_RADIUS_METERS, LOOP_CEILING, CHECKPOINT_SEPARATION_UNITS,
                         CHECKPOINT_SEPARATION_INTERVAL_METERS, CHECKPOINT_CROSSING_THRESHOLD_METERS)


def rotate_list(_list: list, positions: int):
    return _list[-positions:] + _list[:-positions]


def timeit(func):
    def wrapper(*args, **kwargs):
        _start_time = time.perf_counter()
        _r = func(*args, **kwargs)
        _end_time = time.perf_counter()
        _total_time = _end_time - _start_time
        print(f'Function {func.__name__}{args} {kwargs} Took {_total_time:.4f} seconds')
        return _r

    return wrapper


class Telemetry(dict):
    _telemetry_keys = ['lat', 'lon', 'heading', 'groundSpeed', 'altitude', 'battery', 'state']

    def __init__(self):
        dict.__init__(self, zip(self._telemetry_keys, [None]*len(self._telemetry_keys)))

    def set_telemetry(self, lat, lon, heading, groundSpeed, altitude, battery, state):
        self.__setitem__('lat', lat)
        self.__setitem__('lon', lon)
        self.__setitem__('heading', heading)
        self.__setitem__('groundSpeed', groundSpeed)
        self.__setitem__('altitude', altitude)
        self.__setitem__('battery', battery)
        self.__setitem__('state', state)

    @property
    def position(self):
        return self.__getitem__('lat'), self.__getitem__('lon')


class Stopwatch:
    def __init__(self):
        self._start_time: Optional[float] = None
        self._running = False

        self._laps: List[float] = []

    @staticmethod
    def race_format(time_seconds):
        return timedelta(seconds=time_seconds).__str__()

    @property
    def current_time(self):
        return self.race_format(self.current_time_seconds)

    @property
    def current_time_seconds(self):
        if self._running:
            _running_time = time() - self._start_time
            return _running_time

    @property
    def laps(self):
        return self._laps

    def start(self):
        if not self._running:
            self._laps = []
            self._toggle()
            self._start_time = time()

    def lap(self):
        if self._running:
            self._laps.append(self.current_time_seconds)

    def stop(self):
        if self._running:
            _run_time = self.current_time
            self._toggle()
            self._start_time = None
            return _run_time

    def _toggle(self):
        self._running = not self._running


class Tracker:
    def __init__(self, telemetry_info: Telemetry, checkpoints: List[Checkpoint], zone_lengths: List[float]):
        self._telemetry_info = telemetry_info

        checkpoint_list = rotate_list([TrackableCheckpoint(*checkpoint.endpoints) for checkpoint in checkpoints], -1)
        self._checkpoints: List[TrackableCheckpoint] = checkpoint_list
        self._lengths: List[float]
        self._zone_lengths = rotate_list(zone_lengths, 1)

        self._lap: int = 0
        self._zone: int = 0

    def track(self):
        drone_position = Vertex(self._telemetry_info['lat'], self._telemetry_info['lon'])
        next_checkpoint = self._checkpoints[self._zone].midpoint
        distance_to_next_checkpoint = TrackLength.distance(drone_position, next_checkpoint)
        if distance_to_next_checkpoint < CHECKPOINT_CROSSING_THRESHOLD_METERS:
            self.cross_checkpoint()

    def cross_checkpoint(self):
        for index, checkpoint in enumerate(self._checkpoints):
            if not checkpoint.crossed:
                checkpoint.cross()
                print(f'CROSSED CHECKPOINT {index}')
                if index + 1 < len(self._checkpoints):
                    self._zone = index + 1
                else:
                    self._zone = 0
                    self._lap += 1
                    print(f'COMPLETED {self._lap} LAP(S)!')
                return

        for checkpoint in self._checkpoints:
            checkpoint.clear()
        self._checkpoints[0].cross()
        self._zone = 1
        print(f'CROSSED CHECKPOINT 0')

    def calculate_distance_difference(self, other_tracker: Tracker):
        my_distances = self.calculate_distances_to_boundaries()
        other_distances = other_tracker.calculate_distances_to_boundaries()

        my_distance_to_lap = my_distances[1] + self.zone_distances_to_lap()
        other_distance_to_lap = other_distances[1] + other_tracker.zone_distances_to_lap()

        return my_distance_to_lap - other_distance_to_lap

    def zone_distances_to_lap(self):
        return sum(self._zone_lengths[self._zone+1::])

    def calculate_distances_to_boundaries(self):
        drone_position = Vertex(self._telemetry_info['lat'], self._telemetry_info['lon'])
        next_checkpoint = self._checkpoints[self._zone].midpoint
        previous_checkpoint = self._checkpoints[self._zone - 1].midpoint

        distance_to_next = TrackLength.distance(drone_position, next_checkpoint)
        distance_to_previous = TrackLength.distance(previous_checkpoint, drone_position)
        return distance_to_previous, distance_to_next

    def is_ahead_of(self, other_tracker: Tracker):
        laps = self._lap - other_tracker._lap

        if laps > 0:
            return True
        elif laps < 0:
            return False
        else:
            zones = self._zone - other_tracker._zone
            if zones > 0:
                return True
            elif zones < 0:
                return False
            else:
                distance = self.calculate_distance_difference(other_tracker)
                if distance > 0:
                    return True
                else:
                    return False


class Checkpoint:
    def __init__(self, a_vertex: Vertex, b_vertex: Vertex):
        self._a = a_vertex
        self._b = b_vertex

        # Compute midpoint
        _midpoint_lat = (a_vertex.lat + b_vertex.lat) * 0.5
        _midpoint_lon = (a_vertex.lon + b_vertex.lon) * 0.5
        self._midpoint = Vertex(_midpoint_lat, _midpoint_lon)

    @property
    def midpoint(self):
        return self._midpoint

    @property
    def endpoints(self):
        return self._a, self._b


class TrackableCheckpoint(Checkpoint):
    def __init__(self, a_vertex: Vertex, b_vertex: Vertex):
        super().__init__(a_vertex, b_vertex)
        self._crossed = False

    @property
    def crossed(self):
        return self._crossed

    def cross(self):
        self._crossed = True

    def clear(self):
        self._crossed = False


class Seeker:
    def __init__(self, starting_point: Vertex, starting_zone_absolute: int,
                 autopilot_controller, final_height: float):

        self._starting_point = starting_point
        self._starting_zone_absolute = starting_zone_absolute
        self._final_height = final_height
        self._autopilot_controller = autopilot_controller

    @property
    def starting_point(self):
        return self._starting_point

    @property
    def starting_zone_absolute(self):
        return self._starting_zone_absolute

    def _disable_geofence(self):
        self._autopilot_controller.vehicle_geofence_disable()

    def _enable_geofence(self):
        self._autopilot_controller.vehicle_geofence_enable()

    def t_seek_starting_point(self, callback):
        def thread_worker(on_done):
            self.seek_starting_point()
            on_done()

        thread = Thread(target=thread_worker, args=(callback,))
        thread.start()

    def seek_starting_point(self):
        """
        Handles the drone placing at the starting positions
        """
        # DISABLE GEOFENCE
        self._autopilot_controller.vehicle_geofence_disable()
        """ # Somehow the ack messages don't arrive
        while self._autopilot_controller.waiting_parameter_change_ack:
            sleep(0.25)
            self._autopilot_controller.vehicle_geofence_disable()
        """
        # SET ARMABLE MODE
        self._autopilot_controller.vehicle_stabilize()

        # ARM
        self._autopilot_controller.vehicle_arm()

        # TAKEOFF
        self._autopilot_controller.vehicle_take_off(self._final_height)

        # GOTO HOME
        self._autopilot_controller.vehicle_go_to(self._starting_point.lat, self._starting_point.lon)
        while self._autopilot_controller.waiting_go_to:
            sleep(0.25)

        # ENABLE GEOFENCE
        self._autopilot_controller.vehicle_geofence_enable()
        """ # Somehow the ack messages don't arrive
        while self._autopilot_controller.waiting_parameter_change_ack:
            sleep(0.25)
        """


class Racer:
    def __init__(self, id_racer: int, icon_color: str):
        self._id: int = id_racer
        self._icon_color = icon_color

        self._communication_handler = None

        self._autopilot_controller = None
        self._stopwatch: Optional[Stopwatch] = None
        self._tracker: Optional[Tracker] = None
        self._seeker: Optional[Seeker] = None

    @property
    def id(self):
        return self._id

    @property
    def icon_color(self):
        return self._icon_color

    def set_communication_handler(self, communication_handler):
        self._communication_handler = communication_handler

    def set_autopilot_controller(self, autopilot_controller):
        self._autopilot_controller = autopilot_controller

    def set_stopwatch(self, stopwatch: Stopwatch):
        self._stopwatch = stopwatch

    def set_seeker(self, seeker: Seeker):
        self._seeker = seeker

    def set_tracker(self, tracker: Tracker):
        self._tracker = tracker


class Vertex:
    def __init__(self, lat, lon, elevation=None):
        self._lat = lat
        self._lon = lon
        self._elevation = elevation

    @property
    def lat(self):
        return self._lat

    @property
    def lon(self):
        return self._lon

    @property
    def elevation(self):
        return self._elevation

    @property
    def tuple(self):
        return self._lat, self._lon

    @property
    def coordinates(self):
        return self._lat, self._lon, self._elevation

    def __str__(self):
        if self._elevation is None:
            return f'Vertex(lat: {self._lat}, lon: {self._lon})'
        else:
            return f'Vertex(lat: {self._lat}, lon: {self._lon}, elevation: {self._elevation})'


class TrackLength:
    def __init__(self, checkpoints: List[Checkpoint]):
        self._checkpoints = checkpoints
        self._lengths = [0]

        ii_starting_length = 0
        for ii_checkpoint in range(len(self._checkpoints)):
            _current_checkpoint = self._checkpoints[ii_checkpoint]
            try:
                _next_checkpoint = self._checkpoints[ii_checkpoint + 1]
            except IndexError:
                _next_checkpoint = self._checkpoints[0]

            _current_vertex = _current_checkpoint.midpoint
            _next_vertex = _next_checkpoint.midpoint

            _distance = self.distance(_current_vertex, _next_vertex)
            self._lengths.append(_distance + ii_starting_length)
            ii_starting_length += _distance

    @property
    def track_length(self):
        return self._lengths[-1]

    @property
    def lengths(self):
        return self._lengths

    @property
    def checkpoints(self):
        return self._checkpoints

    def distance_to_passed_waypoint(self, distance_meters: float):
        for ii_distance in range(len(self._lengths)):
            try:
                _next_distance = self._lengths[ii_distance + 1]
            except IndexError:
                _next_distance = self._lengths[(ii_distance + 1) % len(self._lengths)]
            if _next_distance > distance_meters:
                return distance_meters - self._lengths[ii_distance]

    def distance_to_next_waypoint(self, distance_meters: float):
        for ii_distance in range(len(self._lengths)):
            try:
                _next_distance = self._lengths[ii_distance + 1]
            except IndexError:
                _next_distance = self._lengths[(ii_distance + 1) % len(self._lengths)]
            if _next_distance > distance_meters:
                return _next_distance - distance_meters

    def zone_boundaries_separation(self, start_distance_meters: float, separation: float):
        _lower_separation = self.distance_to_passed_waypoint(start_distance_meters)
        _upper_separation = self.distance_to_next_waypoint(start_distance_meters)
        return _lower_separation >= separation and _upper_separation >= separation

    def get_track_zone(self, distance_meters: float) -> int:
        _track_lengths = self.lengths
        for ii_index in range(len(_track_lengths)):
            if _track_lengths[ii_index] <= distance_meters < _track_lengths[ii_index + 1]:
                return ii_index

    @staticmethod
    def parametrize(point_start: Vertex, point_end: Vertex):
        _direction_lat = point_end.lat - point_start.lat
        _direction_lon = point_end.lon - point_start.lon
        return lambda _increment: \
            (point_start.lat + _increment * _direction_lat,
             point_start.lon + _increment * _direction_lon)

    @staticmethod
    def distance(point_start: Vertex, point_end: Vertex):
        _start_lat = radians(point_start.lat)
        _end_lat = radians(point_end.lat)

        _lat_diff = _end_lat - _start_lat
        _lon_diff = radians(point_end.lon - point_start.lon)

        _a = sin(_lat_diff / 2) ** 2 + cos(_start_lat) * cos(_end_lat) * sin(_lon_diff / 2) ** 2
        _c = 2 * asin(sqrt(_a))

        _distance = EARTH_RADIUS_METERS * _c
        return _distance


class StartingPoints:
    def __init__(self, track_length: TrackLength, player_count: int):
        self._track_length = track_length

        _racer_separation = track_length.track_length / player_count
        _racer_starting_positions: List[Optional[Vertex]] = [None] * player_count
        _racer_starting_distances: List[Optional[float]] = [None] * player_count
        _racer_starting_zones: List[Optional[int]] = [None] * player_count

        _ii_starting_distance = 0
        _have_separation = False
        _count = 0
        while not _have_separation or _count > LOOP_CEILING:
            _starting_distance = _ii_starting_distance

            # Calculate starting points distances from checkpoint 0
            for _ii_racer in range(player_count):
                _racer_starting_distances[_ii_racer] = _starting_distance + _ii_racer * _racer_separation

            # Check if there is separation between checkpoints
            _separations = [False] * player_count
            for _ii_racer in range(player_count):
                _separations[_ii_racer] = self._track_length.zone_boundaries_separation(_ii_starting_distance,
                                                                                        CHECKPOINT_SEPARATION_UNITS)

            _have_separation = all(_separations)
            _ii_starting_distance += CHECKPOINT_SEPARATION_INTERVAL_METERS
            _count += 1

        for _ii_racer in range(player_count):
            _racer_starting_position, _racer_starting_zone = self._starting_point(
                _racer_starting_distances[_ii_racer])
            _racer_starting_positions[_ii_racer] = _racer_starting_position
            _racer_starting_zones[_ii_racer] = _racer_starting_zone

        self._starting_points = _racer_starting_positions
        self._starting_zones = _racer_starting_zones

    @property
    def starting_points(self):
        return self._starting_points

    @property
    def starting_zones(self):
        return self._starting_zones

    @property
    def track_length(self):
        return self._track_length

    def _starting_point(self, distance_from_start) -> Tuple[Vertex, int]:
        # Compute starting point
        _starting_zone = self._track_length.get_track_zone(distance_from_start)

        _start_checkpoint = self._track_length.checkpoints[_starting_zone]
        try:
            _end_checkpoint = self._track_length.checkpoints[_starting_zone + 1]
        except IndexError:
            _end_checkpoint = self._track_length.checkpoints[(_starting_zone + 1) % len(self._track_length.checkpoints)]

        _parametrizer = self._track_length.parametrize(_start_checkpoint.midpoint, _end_checkpoint.midpoint)

        try:
            _zone_length = self._track_length.lengths[_starting_zone + 1]
        except IndexError:
            _zone_length = self._track_length.lengths[(_starting_zone + 1) % len(self._track_length.lengths)]
        _multiplier = self._track_length.distance_to_passed_waypoint(distance_from_start) / _zone_length
        _starting_point = Vertex(*_parametrizer(_multiplier))
        return _starting_point, _starting_zone


class MavlinkParameters:
    MAV_CMD_NAV_WAYPOINT = '16'
    MAV_CMD_NAV_FENCE_RETURN_POINT = '5000'
    MAV_CMD_NAV_FENCE_POLYGON_VERTEX_INCLUSION = '5001'
    MAV_CMD_NAV_FENCE_POLYGON_VERTEX_EXCLUSION = '5002'
    VERSION = '110'
    FILE_HEADER = f'QGC WPL {VERSION}'
    SEPARATOR = '\t'


class FenceMap:
    def __init__(self):

        self._home: typing.Optional[Vertex] = None
        self._inclusion_zone: typing.Optional[FenceZone] = None
        self._exclusion_zone: typing.Optional[FenceZone] = None

    @property
    def home(self):
        return self._home

    @property
    def inclusion_zone(self):
        return self._inclusion_zone

    @property
    def exclusion_zone(self):
        return self._exclusion_zone

    def __str__(self):
        return f'FenceMap(home: {self._home.__str__()}, ' \
               f'inclusion_zone: {self._inclusion_zone.__str__()}, ' \
               f'exclusion_zone: {self._exclusion_zone.__str__()})'

    def set_home(self, home: Vertex):
        if self._home is None:
            if None not in home.tuple:
                self._home = home
                return True
        return False

    def clear_home(self):
        self._home = None

    def set_inclusion_zone(self, inclusion_zone: FenceZone):
        if self._inclusion_zone is None:
            if inclusion_zone.closed and inclusion_zone.type is True:
                self._inclusion_zone = inclusion_zone
                return True
        return False

    def clear_inclusion_zone(self):
        self._inclusion_zone = None

    def set_exclusion_zone(self, exclusion_zone: FenceZone):
        if self._exclusion_zone is None:
            if exclusion_zone.closed and exclusion_zone.type is False:
                self._exclusion_zone = exclusion_zone
                return True
        return False

    def clear_exclusion_zone(self):
        self._exclusion_zone = None


class FenceZone:
    def __init__(self):
        self._type: typing.Optional[bool] = None  # 0/False: exclusion, 1/True: inclusion
        self._closed: bool = False
        self._vertices: typing.List[Vertex] = []

    @property
    def type(self):
        return self._type

    @property
    def vertices(self):
        return self._vertices

    @property
    def count(self):
        return len(self._vertices)

    @property
    def closed(self):
        return self._closed

    @property
    def tuple_list(self):
        return [_vertex.tuple for _vertex in self._vertices]

    def close(self):
        self._closed = True

    def in_vertices(self, vertex: Vertex):
        for ii_vertex in self._vertices:
            if (ii_vertex.lat == vertex.lat) and (ii_vertex.lon == vertex.lon):
                return True
        return False

    def add_vertex(self, vertex: Vertex):
        if not self._closed:
            if not self.in_vertices(vertex):
                self._vertices.append(vertex)
                return True
        return False

    def set_type(self, zone_type: bool):
        if self._type is None:
            self._type = zone_type
            return True
        return False

    def __str__(self):
        return f'FenceZone(type: {self._type}, closed: {self._closed}, ' \
               f'points: {[_vertex.__str__() for _vertex in self._vertices]})'


class MissionItem:
    def __init__(self, fromstr: typing.Union[str, None] = None,
                 index: typing.Union[str, None] = None,
                 current_wp: typing.Union[str, None] = None,
                 coord_frame: typing.Union[str, None] = None,
                 command: typing.Union[str, None] = None,
                 param1: typing.Union[str, None] = None,
                 param2: typing.Union[str, None] = None,
                 param3: typing.Union[str, None] = None,
                 param4: typing.Union[str, None] = None,
                 param5: typing.Union[str, None] = None,
                 param6: typing.Union[str, None] = None,
                 param7: typing.Union[str, None] = None,
                 autocontinue: typing.Union[str, None] = None):
        if fromstr is None:
            self._index = index
            self._current_wp = current_wp
            self._coord_frame = coord_frame
            self._command = command
            self._params = [param1, param2, param3, param4, param5, param6, param7]
            self._autocontinue = autocontinue
        else:
            if fromstr.endswith('\n'):
                _line = fromstr.strip('\n')
            else:
                _line = fromstr
            _fields = _line.split(MavlinkParameters.SEPARATOR)

            self._index = _fields[0]
            self._current_wp = _fields[1]
            self._coord_frame = _fields[2]
            self._command = _fields[3]
            self._params = _fields[4:11]
            self._autocontinue = _fields[11]

    def valid_home(self):
        if self._command == MavlinkParameters.MAV_CMD_NAV_WAYPOINT and \
                self._current_wp == '1' and \
                all(self._params[-3:]) and \
                self._autocontinue == '1':
            return True
        else:
            return False

    def to_list(self):
        _list = [self._index, self._current_wp, self._coord_frame, self._command, *self._params, self._autocontinue]
        return _list

    def __str__(self):
        return MavlinkParameters.SEPARATOR.join(self.to_list())+'\n'

    @property
    def coordinates(self):
        _lat = float(self._params[-3])
        _lon = float(self._params[-2])
        if self._command == MavlinkParameters.MAV_CMD_NAV_WAYPOINT:
            _elevation = float(self._params[-1])
        else:
            _elevation = None
        return _lat, _lon, _elevation

    @property
    def index(self):
        return self._index

    @property
    def current_wp(self):
        return self._current_wp

    @property
    def coord_frame(self):
        return self._coord_frame

    @property
    def command(self):
        return self._command

    @property
    def params(self):
        return self._params

    @property
    def autocontinue(self):
        return self._autocontinue
