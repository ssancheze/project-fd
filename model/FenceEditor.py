from __future__ import annotations
import typing

from model.fileEditor import FileEditor
from model.FenceClasses import FenceZone, Vertex, MissionItem, MavlinkParameters


class FenceEditor:
    def __init__(self, filepath: str):
        self._filepath = filepath
        self._file_editor: typing.Optional[FileEditor] = FileEditor(filepath)
        self._home: typing.Optional[MissionItem] = None

    @property
    def file_editor(self):
        return self._file_editor

    @property
    def home(self):
        return self._home

    def has_header(self):
        _header = self._file_editor.readline(0).strip('\n')
        if _header == MavlinkParameters.FILE_HEADER:
            return True
        else:
            return False

    def has_home(self):
        _home_item = self._file_editor.readline(1)
        _mission_item = MissionItem(fromstr=_home_item)
        if _mission_item.valid_home():
            return True
        else:
            return False

    def set_home(self, lat, lon, elevation):
        _home = MissionItem(fromstr=None,
                            index='0',
                            current_wp='1',
                            coord_frame='0',
                            command=MavlinkParameters.MAV_CMD_NAV_WAYPOINT,
                            param1='0',
                            param2='0',
                            param3='0',
                            param4='0',
                            param5=str(lat),
                            param6=str(lon),
                            param7=str(elevation),
                            autocontinue='1')
        self._home = _home

    def read_home(self) -> typing.Optional[MissionItem]:
        _home_line = self._file_editor.readline(1)
        if not _home_line:
            return None
        _home_item = MissionItem(fromstr=_home_line)
        return _home_item

    def read_zones(self):
        _ii_index = 2
        _zones = []
        _LINE_COUNT = self._file_editor.len
        while _ii_index < _LINE_COUNT:
            _line = self._file_editor.readline(_ii_index)
            _command = MissionItem(fromstr=_line).command
            if _command == MavlinkParameters.MAV_CMD_NAV_FENCE_POLYGON_VERTEX_EXCLUSION or \
                    _command == MavlinkParameters.MAV_CMD_NAV_FENCE_POLYGON_VERTEX_INCLUSION:
                _zone = self._read_zone(_ii_index)
                _zones.append(_zone)
                _ii_index += _zone.count
            else:
                _ii_index += 1
        return _zones

    def write_home(self) -> bool:
        if self._home is not None:
            _home_line = self._home.__str__()
            self._file_editor.writeline(_home_line)
            return True
        else:
            return False

    def write_header(self):
        _header = MavlinkParameters.FILE_HEADER + '\n'
        self._file_editor.writeline(_header)

    def write_zone(self, zone: typing.List[typing.Tuple[float, float]], zone_type: bool,
                   overwrite_line: typing.Optional[int] = None):
        _file_index = self._get_next_index()
        if _file_index is None:
            return False

        for ii_index, ii_coord_tuple in enumerate(zone):
            self._write_waypoint(ii_coord_tuple, _file_index + ii_index, len(zone), ii_index, zone_type, overwrite_line)

    def write_fence_zone(self, zone: FenceZone, overwrite_line: typing.Optional[int] = None):
        _file_index = self._get_next_index()
        if _file_index is None:
            return False

        for ii_index, ii_vertex in enumerate(zone.vertices):
            self._write_waypoint(ii_vertex.tuple, _file_index + ii_index, zone.count, ii_index, zone.type, overwrite_line)

    def write_zones(self, zones: typing.List[FenceZone]):
        for _ii_zone in zones:
            self.write_fence_zone(_ii_zone)

    def copy_to(self, fence_editor: FenceEditor):
        _zones = self.read_zones()
        _home = self.read_home()
        fence_editor.file_editor.clear_file()
        fence_editor.write_header()
        fence_editor.set_home(*_home.coordinates)
        fence_editor.write_home()
        fence_editor.write_zones(_zones)

    def _read_zone(self, start_line: int):
        _ii_line = start_line
        _ii_item = MissionItem(fromstr=self._file_editor.readline(_ii_line))

        _zone = FenceZone()
        if _ii_item.command == MavlinkParameters.MAV_CMD_NAV_FENCE_POLYGON_VERTEX_EXCLUSION:
            _zone_type = False
        elif _ii_item.command == MavlinkParameters.MAV_CMD_NAV_FENCE_POLYGON_VERTEX_INCLUSION:
            _zone_type = True
        else:
            return None
        _zone.set_type(_zone_type)

        # TODO: Move if needed elsewhere
        def force_int(value: str):
            try:
                _int = int(_ii_item.params[-1])
            except ValueError:
                _int = float(_ii_item.params[-1])
                _int = int(_int)
            return _int

        while _ii_line - force_int(_ii_item.params[-1]) == start_line:
            _lat = float(_ii_item.params[-3])
            _long = float(_ii_item.params[-2])

            _vertex = Vertex(_lat, _long)
            _zone.add_vertex(_vertex)

            # End
            _ii_line += 1
            _item_str = self._file_editor.readline(_ii_line)
            if not _item_str:
                break
            _ii_item = MissionItem(fromstr=_item_str)
        _zone.close()
        return _zone

    def _get_next_index(self):
        _last_line = self._file_editor.read_last_line().strip('\n')
        _last_item = MissionItem(fromstr=_last_line)
        _index = _last_item.index
        if _index is not None:
            return int(_index) + 1
        else:
            return _index

    def _write_waypoint(self, coordinates: typing.Tuple[float, float], index: int, wp_total: int, wp_count: int,
                        fence_type: bool, overwrite_line: typing.Optional[int] = None):
        if fence_type is True:
            _command = MavlinkParameters.MAV_CMD_NAV_FENCE_POLYGON_VERTEX_INCLUSION
        else:
            _command = MavlinkParameters.MAV_CMD_NAV_FENCE_POLYGON_VERTEX_EXCLUSION

        _item = MissionItem(fromstr=None, index=str(index), current_wp='0', coord_frame='3', command=_command,
                            param1=str(wp_total),
                            param2='0',
                            param3='0',
                            param4='0',
                            param5=str(coordinates[0]),
                            param6=str(coordinates[1]),
                            param7=str(wp_count),
                            autocontinue='1'
                            )
        self._file_editor.writeline(_item.__str__(), overwrite_line)

    def _write_item(self, waypoint: MissionItem):
        self._file_editor.writeline(waypoint.__str__())


if __name__ == '__main__':
    import definitions
    import os.path

    copy_fence_name = 'fence_test4.waypoints'
    paste_fence_name = 'fence_test5.waypoints'

    def fence_path(fence_name: str):
        return os.path.join(definitions.FENCES_DIR, fence_name)


    foe = FenceEditor(fence_path(copy_fence_name))
    foe2 = FenceEditor(fence_path(paste_fence_name))
    foe.copy_to(foe2)
