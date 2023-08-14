import tkintermapview

from model.tkintermap.MapModel import MapViewFrameModel


class MapViewFrameController:
    def __init__(self, model: MapViewFrameModel):
        self.model = model

        self._drawing_polygon = False

    @property
    def drawing_polygon(self):
        return self._drawing_polygon

    def get_vertices(self):
        if self._drawing_polygon:
            return self.model.get_idle_polygon()

    def get_idle_polygon(self):
        return self.model.get_idle_polygon()

    def start_polygon(self, coords):
        if not self._drawing_polygon and not self.model.idle_polygon:
            self._drawing_polygon = not self._drawing_polygon
            self.model.new_polygon()
            self.model.add_vertex(coords[0], coords[1])
            print('Drawing...')

    def cancel_polygon(self):
        if self._drawing_polygon:
            self._drawing_polygon = not self._drawing_polygon
            self.model.cancel_polygon()
            print('...Cancelled')

    def close_polygon(self):
        if self._drawing_polygon:
            self.model.close_polygon()

            if self.model.idle_polygon:
                self._drawing_polygon = not self._drawing_polygon
                print('...Closed')

    def polygon_add_vertex(self, coords):
        if self._drawing_polygon:
            self.model.add_vertex(coords[0], coords[1])
            print('Point')

    def polygon_confirm(self, zone_type: bool):
        if not self._drawing_polygon:
            self.model.add_polygon(zone_type)
            print('Polygon Confirmed')

    def polygon_delete(self):
        if not self._drawing_polygon:
            self.model.del_polygon()
            print('Polygon Deleted')

    def save_map(self):
        pass

    def load_map(self):
        pass

    def clear_map(self):
        pass

    def change_tile_set(self, selected_tile):
        self.model.set_tile_server(selected_tile)

    def get_tile_set(self):
        return self.model.tile_server, self.model.max_zoom


if __name__ == '__main__':
    pass
