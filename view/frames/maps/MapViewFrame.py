import os.path
import tkintermapview

from view.frames.BasicFrame import BasicFrame
from view.frames.maps.MapBasicControlFrame import MapBasicControlFrame
import config
from definitions import MAPS_DIR, EETAC_COORDINATES

MAP_VIEW_DATABASE_PATH = os.path.join(MAPS_DIR, 'offline_tiles_eetac_gsat.db')


class MapViewFrame(BasicFrame):
    def __init__(self, master=None, __controls=None):
        super().__init__(master, grid=(2, 1))
        self.frame.rowconfigure(0, weight=8)

        # Map view widget
        if config.map_offline_mode is True:
            self.map_view = tkintermapview.TkinterMapView(master=self.frame, corner_radius=60, use_database_only=True,
                                                          database_path=MAP_VIEW_DATABASE_PATH)
        else:
            self.map_view = tkintermapview.TkinterMapView(master=self.frame, corner_radius=60)

        # Set default position
        self.map_view.set_position(*EETAC_COORDINATES)

        # TODO: Lock zoom

        # End
        self.place_in_grid(self.map_view, (0, 0))

        # Map controls frame
        if __controls:
            self.control_frame = __controls(self.frame, self.map_view)
            self.control_frame.on_tile_set_change('gsat')
            # End
            self.place_in_grid(self.control_frame.frame, (1, 0))
        else:
            self.control_frame = None

        # End
        self.pack_frame()

    def set_control_frame(self, control_frame: type(MapBasicControlFrame), controller):
        self.control_frame = control_frame(self.frame, self.map_view, controller)
        self.control_frame.on_tile_set_change('gsat')
        # End
        self.place_in_grid(self.control_frame.frame, (1, 0))


if __name__ == '__main__':
    from view import MyTk
    from view.frames.maps.MapViewControlFrames import MapFenceLoaderControlFrame

    def main():
        win = MyTk.Window()
        win.config()
        MapViewFrame(win, MapFenceLoaderControlFrame)
        win.mainloop()

    main()
