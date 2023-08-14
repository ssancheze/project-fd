from FileHandler import FileHandler
import typing


class MavlinkParameters:
    MAV_CMD_NAV_WAYPOINT = '16'
    MAV_CMD_NAV_FENCE_RETURN_POINT = '5000'
    MAV_CMD_NAV_FENCE_POLYGON_VERTEX_INCLUSION = '5001'
    MAV_CMD_NAV_FENCE_POLYGON_VERTEX_EXCLUSION = '5002'
    VERSION = '110'
    FILE_HEADER = f'QGC WPL {VERSION}'
    SEPARATOR = '\t'


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

    def to_list(self):
        _list = [self._index, self._current_wp, self._coord_frame, self._command, *self._params, self._autocontinue]
        return _list

    def __str__(self):
        return MavlinkParameters.SEPARATOR.join(self.to_list())


class FenceFileManager:
    MAVLINK_PARAMETERS = MavlinkParameters

    def __init__(self):
        self._file_handler: typing.Optional[FileHandler] = None
        self._filepath: typing.Optional[str] = None
        self._start_waypoint: typing.Optional[typing.List[float]] = None

    @property
    def filepath(self):
        return self._filepath

    @property
    def start_waypoint(self):
        return self._start_waypoint

    def set_start_waypoint(self, lat: float, lon: float, elevation: float):
        self._start_waypoint = [lat, lon, elevation]

    def open_file(self, filepath: str):
        self._filepath = filepath
        self._file_handler = FileHandler(filepath, separator=self.MAVLINK_PARAMETERS.SEPARATOR)

    def write_zone(self, waypoint_list: typing.List[typing.Tuple[float, float]], zone_type: int = 0):
        """
        :param waypoint_list: list of coordinates in format tuple(lat, lon)
        :param zone_type: 0: exclusion, 1: inclusion
        """
        _waypoint_count = len(waypoint_list)
        if zone_type == 0:
            _command = MavlinkParameters.MAV_CMD_NAV_FENCE_POLYGON_VERTEX_EXCLUSION
        elif zone_type == 1:
            _command = MavlinkParameters.MAV_CMD_NAV_FENCE_POLYGON_VERTEX_INCLUSION

        _file_index = self._file_handler.line_count
        if _file_index > 0:
            if _file_index == 1:
                if self.file_handler.file_reader.readline(0) != MavlinkParameters.FILE_HEADER:
                    raise Exception(f'{self.filepath} format invalid')
                self._write_start_waypoint()
            elif _file_index == 2:
                _file_index -= 1  # Subtract the header

        else:
            self._write_header()
            self._write_start_waypoint()
            _file_index = 1

        for _index, _waypoint in enumerate(waypoint_list):
            _mission_item = MissionItem(fromstr=None,
                                        index=str(_file_index+_index),
                                        current_wp='0',
                                        coord_frame='3',
                                        command=_command,
                                        param1=str(_waypoint_count),
                                        param2='0',
                                        param3='0',
                                        param4='0',
                                        param5=str(_waypoint[0]),
                                        param6=str(_waypoint[1]),
                                        param7=str(_index),
                                        autocontinue='1')
            self._file_handler.write(str(_mission_item))

    def _write_header(self):
        self._file_handler.write(self.MAVLINK_PARAMETERS.FILE_HEADER)

    def _write_start_waypoint(self):
        if self._start_waypoint is None:
            raise AttributeError('\'start_waypoint\' not defined')
        _mission_item = MissionItem(fromstr=None,
                                    index='0',
                                    current_wp='1',
                                    coord_frame='0',
                                    command=MavlinkParameters.MAV_CMD_NAV_WAYPOINT,
                                    param1='0',
                                    param2='0',
                                    param3='0',
                                    param4='0',
                                    param5=str(self._start_waypoint[0]),
                                    param6=str(self._start_waypoint[1]),
                                    param7=str(self._start_waypoint[2]),
                                    autocontinue='1')
        self._file_handler.write(str(_mission_item))

    def _write_waypoint(self, mission_item: MissionItem):
        _line = str(mission_item)
        self._file_handler.write(_line)

    @property
    def file_handler(self):
        return self._file_handler


if __name__ == '__main__':
    my_manager = FenceFileManager()

    my_zone = [(41.27622914, 1.98852673),
               (41.27642164, 1.98845029),
               (41.27647909, 1.98874265),
               (41.27636520, 1.98879227),
               (41.27640955, 1.98900416),
               (41.27633900, 1.98904306)]

    def main():
        my_manager.open_file('fence_test5.waypoints')
        my_manager.set_start_waypoint(41.2763194, 1.9886342, 3.860000)
        my_manager.write_zone(my_zone)
        my_manager.file_handler.read(3)

    def main2():
        lines1 = open('../dev/fence_test5 - copia.waypoints', 'r').read()
        lines2 = open('../dev/fence_test5.waypoints', 'r').read()

    main()
    print(0)
