import typing
import numpy as np

from model.BasicModel import BasicModel as _BasicModel
from model.FenceEditor import FenceEditor as _FenceEditor
from model.FenceClasses import Vertex as _Vertex
from model.FenceClasses import FenceZone as _FenceZone
from model.FenceClasses import FenceMap as _FenceMap
from model.FenceClasses import Checkpoint as _Checkpoint
from model.RaceClasses import Racer as _Racer
from model.RaceClasses import Stopwatch as _Stopwatch
from model.RaceClasses import TrackLength as _TrackLength
from model.RaceClasses import StartingPoints as _StartingPoints
from model.tkintermap.MapViewElevationRequest import get_elevation as _get_elevation
from model.tkintermap.MapViewTileServers import get_tile_server as _get_tile_server


class BasicMapViewModel(_BasicModel):
    """
    MapView basic model class. Stores the map tile set
    """
    def __init__(self):
        self._tile_server_address: typing.Optional[str] = None
        self._tile_server_max_zoom: typing.Optional[int] = None

    @property
    def tile_server(self):
        return self._tile_server_address, self._tile_server_max_zoom

    def set_tile_server(self, tile_server: str):
        self._tile_server_address, self._tile_server_max_zoom = _get_tile_server(tile_server)


class FenceLoaderModel(_BasicModel):

    """
    Model class for loading .waypoints fence files.
    Attributes:
        _map    FenceMap instance which has exactly 2 zones (inclusion and exclusion) and a home Vertex
        _file_manager   FenceEditor instance to read files
    """
    def __init__(self):

        _BasicModel.__init__(self)

        self._file_manager: typing.Optional[_FenceEditor] = None
        self._map: typing.Optional[_FenceMap] = None

    @property
    def map(self):
        return self._map

    def open_map_from_file(self, open_dir: str):
        # Open file with FenceEditor
        self._file_manager = _FenceEditor(open_dir)

        # New map instance
        _map = _FenceMap()

        # Read and set file's home's coordinates
        _coordinates = self._file_manager.read_home().coordinates
        _home_vertex = _Vertex(*_coordinates)
        if not _map.set_home(_home_vertex):
            return False

        # Read and add file's zones
        _zones = self._file_manager.read_zones()
        if len(_zones) != 2:
            return False
        for _ii_zone in _zones:
            if _ii_zone.type is True:
                if not _map.set_inclusion_zone(_ii_zone):
                    return False
            if _ii_zone.type is False:
                if not _map.set_exclusion_zone(_ii_zone):
                    return False

        # Set map and clear FenceEditor
        self._map = _map
        self._file_manager = None

        # Successful process return
        return True

    def clear_map(self):
        self._map = None


class FenceEditorModel(FenceLoaderModel):
    """
    Fence editor model class.
    """
    def __init__(self):
        FenceLoaderModel.__init__(self)

        self._polygon: typing.Optional[_FenceZone] = None

    @property
    def idle_polygon(self):
        return self._polygon

    @property
    def closed_polygon(self):
        if self._polygon is not None:
            return self._polygon.closed
        else:
            return False

    def set_home(self, home_vertex: _Vertex):
        self._map.set_home(home_vertex)

    def clear_home(self):
        if self._map:
            self._map.clear_home()

    def new_map(self):
        if self._map is None:
            self._map = _FenceMap()
            return True
        return False

    def new_polygon(self):
        if self._polygon is None:
            if self._map:
                if self._map.exclusion_zone is None or self._map.inclusion_zone is None:
                    self._polygon = _FenceZone()
                    return True
            else:
                self._polygon = _FenceZone()
                return True
        return False

    def add_vertex(self, vertex: _Vertex):
        if self._polygon is not None:
            if not self._polygon.closed:
                self._polygon.add_vertex(vertex)
                return True
        return False

    def close_polygon(self):
        if self._polygon is not None:
            if not self._polygon.closed:
                if self._polygon.count > 2:
                    self._polygon.close()
                    return True
        return False

    def cancel_polygon(self):
        if self._polygon is not None:
            if not self._polygon.closed:
                self._polygon = None
                return True
        return False

    def add_polygon(self, zone_type: bool):
        # If there is a close polygon, set type
        if self._polygon is not None:
            if self._polygon.closed:
                self._polygon.set_type(zone_type)
            else:
                return False
        else:
            return False

        # If no map, create one
        if self._map is None:
            self.new_map()

        # Check if map already has zone
        if zone_type is True:
            if self._map.set_inclusion_zone(self._polygon):
                self._polygon = None
                return True
            else:
                return False
        else:
            if self._map.set_exclusion_zone(self._polygon):
                self._polygon = None
                return True
            else:
                return False

    def clear_polygon(self):
        if self._polygon is not None:
            if self._polygon.closed:
                self._polygon = None
                return True
        return False

    def clear_map_inclusion_zone(self):
        if self._map:
            self._map.clear_inclusion_zone()

    def clear_map_exclusion_zone(self):
        if self._map:
            self._map.clear_exclusion_zone()

    def save_to_file(self, save_dir: str):
        # Open file with FenceEditor
        self._file_manager = _FenceEditor(save_dir)

        # If file already exists, clear it
        self._file_manager.file_editor.clear_file()

        # Write file header
        self._file_manager.write_header()

        # Get home coordinates and elevation
        _home_lat, _home_lon = self._map.home.tuple
        _home_elevation = _get_elevation(_home_lat, _home_lon)

        # Set and write home
        self._file_manager.set_home(_home_lat, _home_lon, _home_elevation)
        self._file_manager.write_home()

        # Write all zones
        self._file_manager.write_zones([self._map.inclusion_zone, self._map.exclusion_zone])

        # Success exit code
        return True


class FenceCheckpointModel(FenceLoaderModel):
    """
    Fence checkpoint handler class.
    """
    def __init__(self):
        FenceLoaderModel.__init__(self)

        self._checkpoints: typing.List[_Checkpoint] = []

    @property
    def checkpoints(self):
        return self._checkpoints

    def create_checkpoints(self):
        # Check if map exists
        if self._map is None:
            return False

        # Get both zones
        _exclusion_zone = self._map.exclusion_zone
        _inclusion_zone = self._map.inclusion_zone

        _exclusion_zone_vertices_array = np.array(_exclusion_zone.tuple_list)
        _checkpoints = []

        for _ii_inclusion_vertex in _inclusion_zone.vertices:
            _inclusion_vertex_arr = np.array(_ii_inclusion_vertex.tuple)
            _distances = np.linalg.norm(_exclusion_zone_vertices_array - _inclusion_vertex_arr, axis=1)
            _min_index = np.argmin(_distances)
            _a_list: typing.Union[list, object] = _inclusion_vertex_arr.tolist()
            _b_list: typing.Union[list, object] = _exclusion_zone_vertices_array[_min_index].tolist()
            _a_vertex = _Vertex(_a_list[0], _a_list[1])
            _b_vertex = _Vertex(_b_list[0], _b_list[1])
            _checkpoint = _Checkpoint(_a_vertex, _b_vertex)
            _checkpoints.append(_checkpoint)

        self._checkpoints = _checkpoints

    def clear_checkpoints(self):
        self._checkpoints = []


class RaceModel(FenceCheckpointModel):
    def __init__(self):
        """
        Race handler
        """
        FenceCheckpointModel.__init__(self)

        self._track_length: typing.Optional[_TrackLength] = None
        self._starting_points: typing.Optional[_StartingPoints] = None

    @property
    def track_length(self):
        return self._track_length

    @property
    def starting_points(self):
        return self._starting_points

    def create_checkpoints(self):
        super().create_checkpoints()

        self._track_length = _TrackLength(self.checkpoints)

        self._starting_points = _StartingPoints(self._track_length)
