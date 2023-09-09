import typing
import os.path

from controller.BasicController import BasicController
from model.MapViewModels import BasicMapViewModel, FenceLoaderModel, FenceEditorModel, FenceCheckpointModel
from model.maps.MapViewTileServers import map_tiles_dict
from model.utils import Vertex
from definitions import FENCES_DIR


class MapViewBasicController(BasicController):
    def __init__(self):
        """
        Base MapView controller class.
        """
        BasicController.__init__(self)

        self._model = BasicMapViewModel()

    def change_tile_set(self, tile_set: str):
        _addresses = map_tiles_dict()
        if tile_set+'_address' in _addresses:
            self._model.set_tile_server(tile_set)

    def get_tile_set(self):
        return self._model.tile_server


class FenceLoaderController(BasicController):
    def __init__(self):
        """
        FenceLoader controller class
        """
        BasicController.__init__(self)

        self._model = FenceLoaderModel()

    def get_map(self):
        return self._model.map

    def open_map_from_file(self, open_path: str):
        self._model.clear_map()
        if os.path.isfile(open_path):
            if self._model.open_map_from_file(open_path):
                return True
            else:
                return False
        else:
            return False

    def clear_map(self):
        self._model.clear_map()


class FenceEditorController(FenceLoaderController):
    def __init__(self):
        """
        Fence editor controller class
        """
        FenceLoaderController.__init__(self)

        self._model = FenceEditorModel()
        self._drawing = False

    def set_home(self, home_coordinates: typing.Tuple[float, float]):
        # Request home coordinates
        _home_lat = home_coordinates[0]
        _home_lon = home_coordinates[1]

        # Make home waypoint and set it in the model
        _home_vertex = Vertex(_home_lat, _home_lon)

        # If no map, create new
        if not self._model.map:
            self._model.new_map()
            self._model.set_home(_home_vertex)
        else:
            # Set home if only no home set
            if not self._model.map.home:
                self._model.set_home(_home_vertex)

    def get_home(self):
        return self._model.map.home

    def get_idle(self):
        _idle_polygon = self._model.idle_polygon
        if _idle_polygon is None:
            return None
        else:
            _polygon_dict = {
                'closed': _idle_polygon.closed,
                'vertices': _idle_polygon.vertices
            }
            return _polygon_dict

    def start_polygon(self, coordinates):
        if not self._drawing:
            if self._model.new_polygon():
                _waypoint_vertex = Vertex(coordinates[0], coordinates[1])
                self._model.add_vertex(_waypoint_vertex)
                self._drawing = True

    def add_waypoint(self, coordinates):
        if self._drawing:
            _waypoint_vertex = Vertex(coordinates[0], coordinates[1])
            self._model.add_vertex(_waypoint_vertex)

    def close_polygon(self):
        if self._drawing:
            if self._model.close_polygon():
                self._drawing = False

    def cancel_polygon(self):
        if self._drawing:
            if self._model.cancel_polygon():
                self._drawing = False

    def add_idle_to_map(self, zone_type: bool):
        if not self._drawing:
            self._model.add_polygon(zone_type)

    def clear_idle(self):
        if not self._drawing:
            self._model.clear_polygon()

    def clear_map_inclusion_zone(self):
        if not self._drawing:
            self._model.clear_map_inclusion_zone()

    def clear_map_exclusion_zone(self):
        if not self._drawing:
            self._model.clear_map_exclusion_zone()

    def clear_home(self):
        self._model.clear_home()

    def can_save_map(self):
        if not self._drawing:
            if not self._model.idle_polygon:
                if self._model.map.home is not None:
                    if self._model.map.inclusion_zone is not None and self._model.map.exclusion_zone is not None:
                        return True
        return False

    def open_map_from_file(self, open_path: str):
        self.cancel_polygon()
        self.clear_idle()
        FenceLoaderController.open_map_from_file(self, open_path)

    def save_to_file(self, save_path: str):
        if self._model.save_to_file(save_path):
            print('File saved successfully')
        else:
            print('Could not save file')


class FenceCheckpointController(FenceLoaderController):
    def __init__(self):
        """
        Fence checkpoint generator controller class
        """
        FenceLoaderController.__init__(self)

        self._model = FenceCheckpointModel()

    def get_checkpoints(self):
        return self._model.checkpoints

    def create_checkpoints(self):
        self._model.create_checkpoints()

    def clear_checkpoints(self):
        self._model.clear_checkpoints()

    def open_map_from_file(self, open_path: str):
        open_path = os.path.join(FENCES_DIR, open_path)
        self.clear_checkpoints()
        super().open_map_from_file(open_path)
