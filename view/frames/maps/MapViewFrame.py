import os.path
import tkintermapview

from view.frames.BasicFrame import BasicFrame
import config
from model.tkintermap import MapViewTileServers as Tiles
from definitions import MAPS_DIR
from view.frames.maps.MapFenceControlsFrame import MapFenceControlsFrame
from controller.MapViewController import MapViewFrameController

MAP_VIEW_DATABASE_PATH = os.path.join(MAPS_DIR, 'offline_tiles_eetac_gsat.db')


class MapViewFrame(BasicFrame):
    def __init__(self, master=None, controller: MapViewFrameController = None):
        super().__init__(master, grid=(2, 1))
        self.frame.rowconfigure(0, weight=8)
        self.controller = controller

        # Map view widget
        if config.map_offline_mode is True:
            self.map_view = tkintermapview.TkinterMapView(master=self.frame, corner_radius=60, use_database_only=True,
                                                          database_path=MAP_VIEW_DATABASE_PATH)
        else:
            self.map_view = tkintermapview.TkinterMapView(master=self.frame, corner_radius=60)

        # TODO: Remove position placeholder
        self.map_view.set_position(41.27641629296008, 1.9886751866535248)

        # TODO: Lock zoom

        # End
        self.place_in_grid(self.map_view, (0, 0))

        # Map controls frame
        self.controls_frame = MapFenceControlsFrame(self.frame, self.map_view, self.controller)
        self.controls_frame.set_tile_server(*Tiles.method_get_tile_server('gsat'))

        # End
        self.place_in_grid(self.controls_frame.frame, (1, 0))

        # End
        self.pack_frame()


if __name__ == '__main__':
    from view import MyTk
    from model.tkintermap.MapViewModel import MapViewFrameModel

    def main():
        win = MyTk.Window()
        win.config()
        y = win.tk.geometry()
        map_model = MapViewFrameModel()
        map_controller = MapViewFrameController(map_model)
        MapViewFrame(win, map_controller)
        win.mainloop()

    main()
