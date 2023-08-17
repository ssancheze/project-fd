from __future__ import annotations
import typing


# TODO: move to definitions
class MavlinkParameters:
    MAV_CMD_NAV_WAYPOINT = '16'
    MAV_CMD_NAV_FENCE_RETURN_POINT = '5000'
    MAV_CMD_NAV_FENCE_POLYGON_VERTEX_INCLUSION = '5001'
    MAV_CMD_NAV_FENCE_POLYGON_VERTEX_EXCLUSION = '5002'
    VERSION = '110'
    FILE_HEADER = f'QGC WPL {VERSION}'
    SEPARATOR = '\t'


class FenceZone:
    def __init__(self):
        self._type: typing.Optional[bool] = None  # 0/False: exclusion, 1/True: inclusion
        self._closed: bool = False
        self._vertices: typing.List[Vertex] = []

    def in_vertices(self, vertex: Vertex):
        for ii_vertex in self._vertices:
            if (ii_vertex.lat == vertex.lat) and (ii_vertex.lon == vertex.lon):
                return True
        return False

    def add_vertex(self, vertex: Vertex):
        if not self.in_vertices(vertex):
            self._vertices.append(vertex)

    def set_type(self, zone_type: bool):
        if self._type is None:
            self._type = zone_type

    def __str__(self):
        return f'FenceZone(type: {self._type}, closed: {self._closed}, ' \
               f'points: {[_vertex.__str__() for _vertex in self._vertices]})'

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


class Vertex:
    def __init__(self, lat, lon, elevation=None):
        self._lat = lat
        self._lon = lon
        self._elevation = elevation

    def __str__(self):
        if self._elevation is None:
            return f'Vertex(lat: {self._lat}, lon: {self._lon})'
        else:
            return f'Vertex(lat: {self._lat}, lon: {self._lon}, elevation: {self._elevation})'

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
