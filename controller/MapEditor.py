import tkintermapview
import typing
import numpy as np

_MarkerClass = tkintermapview.map_widget.CanvasPositionMarker
_THRESHOLD = 0.005
_EARTH_RADIUS = 6371E3


# STATIC METHODS
def above_threshold(vector1: np.ndarray, vector2: np.ndarray, threshold: float):
    vector_dif = vector1 - vector2
    vector_dot = np.dot(vector_dif, vector_dif)
    threshold2 = threshold**2
    return vector_dot >= threshold2


def marker_is_valid(marker: _MarkerClass):
    pass


class PolygonMaker:
    def __init__(self):
        self._marker_list: typing.List[_MarkerClass] = list()
        self._polygon: typing.List[np.ndarray] = list()
        self._count: int = 0
        self._drawing: bool = False

    # PROPERTIES
    @property
    def count(self):
        return self._count

    @property
    def polygon(self):
        return self._polygon

    def list_is_empty(self):
        return not bool(self._count)

    # ADD/REMOVE MARKERS
    def add_marker(self, marker: _MarkerClass):
        self._marker_list.append(marker)

        _marker_vector = np.array(marker.position)
        self._polygon.append(_marker_vector)

        self._count += 1

    def remove_marker(self, position: int):
        self._marker_list.pop(position)
        self._polygon.pop(position)

        self._count -= 1

    # MANAGE POLYGON
    def start_polygon(self, zeroth_marker: _MarkerClass):
        if self.list_is_empty() and not self._drawing:
            self.add_marker(zeroth_marker)
            self._drawing = True

    def continue_polygon(self, new_marker: _MarkerClass):
        if self._drawing:
            if marker_is_valid(new_marker):
                self.add_marker(new_marker)

    def finish_polygon(self):
        self._drawing = False

    def clear_polygon(self):
        while not self.list_is_empty():
            self.remove_marker(-1)


if __name__ == '__main__':
    pass
