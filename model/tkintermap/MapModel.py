from __future__ import annotations
import typing


from model.tkintermap import MapViewTileServers


class MapViewFrameModel:
    def __init__(self):
        self._tile_server: typing.Optional[str] = None
        self._max_zoom: typing.Optional[int] = None
        self._zones: typing.List[FenceZone] = []
        self._polygon: typing.Optional[FenceZone] = None

    @property
    def tile_server(self):
        return self._tile_server

    @property
    def max_zoom(self):
        return self._max_zoom

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

    def del_polygon(self):
        if self._polygon is not None:
            if self._polygon.closed:
                self._polygon = None


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

    def close(self):
        self._closed = True


class Vertex:
    def __init__(self, lat, lon):
        self._lat = lat
        self._lon = lon

    @property
    def lat(self):
        return self._lat

    @property
    def lon(self):
        return self._lon
