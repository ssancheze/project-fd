from __future__ import annotations
import typing


from model.tkintermap import MapViewTileServers
from model.tkintermap.MapViewElevationRequest import get_elevation
from model.FenceClasses import FenceZone, Vertex
from model.FenceEditor import FenceEditor


class MapViewFrameModel:
    def __init__(self):
        self._tile_server: typing.Optional[str] = None
        self._max_zoom: typing.Optional[int] = None
        self._home: typing.Optional[Vertex] = None
        self._zones: typing.List[FenceZone] = []
        self._polygon: typing.Optional[FenceZone] = None
        self._file_manager: typing.Optional[FenceEditor] = None

    @property
    def tile_server(self):
        return self._tile_server

    @property
    def max_zoom(self):
        return self._max_zoom

    @property
    def zones(self):
        return self._zones

    @property
    def file_manager(self):
        return self._file_manager

    @property
    def home(self):
        return self._home

    @property
    def idle_polygon(self):
        if self._polygon is not None:
            return self._polygon.closed
        else:
            return False

    def set_tile_server(self, selected_tile):
        self._tile_server, self._max_zoom = MapViewTileServers.method_get_tile_server(selected_tile)

    def get_idle_polygon(self):
        return self._polygon

    def set_home(self, coords):
        _home_vertex = Vertex(*coords)
        self._home = _home_vertex

    def new_polygon(self):
        if self._polygon is None:
            self._polygon = FenceZone()

    def add_vertex(self, lat: float, long: float):
        if self._polygon is not None:
            if not self._polygon.closed:
                _vertex = Vertex(lat, long)
                self._polygon.add_vertex(_vertex)

    def close_polygon(self):
        if self._polygon is not None:
            if not self._polygon.closed:
                if self._polygon.count > 2:
                    self._polygon.close()

    def cancel_polygon(self):
        if self._polygon is not None:
            if not self._polygon.closed:
                self._polygon = None

    def add_polygon(self, zone_type: bool):
        if self._polygon is not None:
            if self._polygon.closed:
                self._polygon.set_type(zone_type)
                self._zones.append(self._polygon)
                self._polygon = None
                return True
        return False

    def del_polygon(self):
        if self._polygon is not None:
            if self._polygon.closed:
                self._polygon = None

    def clear_all(self):
        self._polygon = None
        self._zones = []
        self._home = None

    def save_to_file(self, save_dir: str):
        self._file_manager = FenceEditor(save_dir)
        self._file_manager.file_editor.clear_file()
        self._file_manager.write_header()
        _home_lat, _home_lon = self._home.tuple
        _home_elevation = get_elevation(_home_lat, _home_lon)
        self._file_manager.set_home(_home_lat, _home_lon, _home_elevation)
        self._file_manager.write_home()
        self._file_manager.write_zones(self._zones)
        return True

    def open_file(self, open_dir: str):
        self._file_manager = FenceEditor(open_dir)
        _coordinates = self._file_manager.read_home().coordinates
        self.set_home(_coordinates)
        _zones = self._file_manager.read_zones()
        for _ii_zone in _zones:
            self._zones.append(_ii_zone)
        self._file_manager = None
        return True


if __name__ == '__main__':
    pass
