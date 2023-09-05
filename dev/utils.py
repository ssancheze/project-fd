from math import radians, sin, cos, asin, sqrt
from typing import Optional, List, Tuple
from datetime import timedelta
from time import time

from definitions import (EARTH_RADIUS_METERS, MAX_RACERS, LOOP_CEILING, CHECKPOINT_SEPARATION_UNITS,
                         CHECKPOINT_SEPARATION_INTERVAL_METERS)
from model.MQTTMessageHandler import CommunicationModeHandler, AutopilotServiceController


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
    pass


class Racer:
    def __init__(self, id_racer: int):
        self._id: int = id_racer
        self._telemetry_info: Optional[Telemetry] = None
        self._ready: bool = False

        self._communication_handler = None

        self._autopilot_controller: Optional[AutopilotServiceController] = None
        self._stopwatch: Optional[Stopwatch] = None
        self._tracker: Optional[Tracker] = None

    @property
    def id(self):
        return self._id

    @property
    def telemetry_info(self):
        return self._telemetry_info

    @property
    def ready(self):
        return self._ready

    def set_ready(self):
        self._ready = True

    def unset_ready(self):
        self._ready = False

    def set_telemetry_info(self, telemetry_info: Telemetry):
        self._telemetry_info = telemetry_info

    def set_communication_handler(self, communication_handler: CommunicationModeHandler):
        self._communication_handler = communication_handler

    def set_autopilot_controller(self, autopilot_controller: AutopilotServiceController):
        self._autopilot_controller = autopilot_controller

    def set_stopwatch(self, stopwatch: Stopwatch):
        self._stopwatch = stopwatch

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
    def __init__(self, track_length: TrackLength):
        self._track_length = track_length

        _racer_separation = track_length.track_length / MAX_RACERS
        _racer_starting_positions: List[Optional[Vertex]] = [None] * MAX_RACERS
        _racer_starting_distances: List[Optional[float]] = [None] * MAX_RACERS
        _racer_starting_zones: List[Optional[int]] = [None] * MAX_RACERS

        _ii_starting_distance = 0
        _have_separation = False
        _count = 0
        while not _have_separation or _count > LOOP_CEILING:
            _starting_distance = _ii_starting_distance

            # Calculate starting points distances from checkpoint 0
            for _ii_racer in range(MAX_RACERS):
                _racer_starting_distances[_ii_racer] = _starting_distance + _ii_racer * _racer_separation

            # Check if there is separation between checkpoints
            _separations = [False] * MAX_RACERS
            for _ii_racer in range(MAX_RACERS):
                _start_distance = _racer_starting_distances[_ii_racer]
                _lower_separation = self._track_length.distance_to_passed_waypoint(_start_distance)
                _upper_separation = self._track_length.distance_to_next_waypoint(_start_distance)
                _separations[_ii_racer] = (_lower_separation >= CHECKPOINT_SEPARATION_UNITS and
                                           _upper_separation >= CHECKPOINT_SEPARATION_UNITS)

            _have_separation = all(_separations)
            _ii_starting_distance += CHECKPOINT_SEPARATION_INTERVAL_METERS
            _count += 1

        for _ii_racer in range(MAX_RACERS):
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
    def track_length(self):
        return self._track_length

    @staticmethod
    def _parametrize(point_start: Vertex, point_end: Vertex):
        _direction_lat = point_end.lat - point_start.lat
        _direction_lon = point_end.lon - point_start.lon
        return lambda _increment: \
            (point_start.lat + _increment * _direction_lat,
             point_start.lon + _increment * _direction_lon)

    def _have_separation(self, point: Vertex, zone: int):
        _lower_midpoint = self._track_length.checkpoints[zone].midpoint
        try:
            _upper_midpoint = self._track_length.checkpoints[zone + 1].midpoint
        except IndexError:
            _upper_midpoint = self._track_length.checkpoints[0].midpoint

        _lower_separation = self._track_length.distance(point, _lower_midpoint)
        _upper_separation = self._track_length.distance(point, _upper_midpoint)
        _separation = (_lower_separation >= CHECKPOINT_SEPARATION_UNITS and
                       _upper_separation >= CHECKPOINT_SEPARATION_UNITS)
        return _separation

    def _get_track_zone(self, distance_meters: float) -> int:
        _track_lengths = self._track_length.lengths
        for ii_index in range(len(_track_lengths)):
            if _track_lengths[ii_index] <= distance_meters < _track_lengths[ii_index + 1]:
                return ii_index

    def _starting_point(self, distance_from_start) -> Tuple[Vertex, int]:
        # Compute starting point
        _starting_zone = self._get_track_zone(distance_from_start)
        _start_checkpoint = self._track_length.checkpoints[_starting_zone]
        try:
            _end_checkpoint = self._track_length.checkpoints[_starting_zone + 1]
        except IndexError:
            _end_checkpoint = self._track_length.checkpoints[(_starting_zone + 1) % len(self._track_length.checkpoints)]

        _parametrizer = self._parametrize(_start_checkpoint.midpoint, _end_checkpoint.midpoint)
        try:
            _zone_length = self._track_length.lengths[_starting_zone + 1]
        except IndexError:
            _zone_length = self._track_length.lengths[(_starting_zone + 1) % len(self._track_length.lengths)]
        _multiplier = self._track_length.distance_to_passed_waypoint(distance_from_start) / _zone_length
        _starting_point = Vertex(*_parametrizer(_multiplier))
        return _starting_point, _starting_zone
