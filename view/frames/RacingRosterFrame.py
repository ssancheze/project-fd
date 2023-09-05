import tkinter as tk
import tkinter.ttk as ttk
import os.path

from view.frames.BasicFrame import RowFrame, RowFrameRow
from controller.RaceController import RaceController
from model.RaceClasses import Racer
from definitions import ASSETS_DIR, MAX_RACERS


class RacingRosterFrame(RowFrame):
    def __init__(self, master, race_controller: RaceController):
        super().__init__(master, rows=MAX_RACERS, label='ORDER')

        self.controller = race_controller

        racers = self.controller.get_players_list()
        for ii_racer in racers:
            self.add_row(PlayerRow(self.frame, ii_racer, self.controller))

        self.pack_rows()
        self.update_rows()
        self.pack_frame()


class PlayerRow(RowFrameRow):
    default_player_icon_path = os.path.join(ASSETS_DIR, 'user_default.png')
    default_username = 'racer_'

    def __init__(self, master, racer: Racer, race_controller: RaceController):
        super().__init__(master)

        self.controller = race_controller
        self._racer = racer

        # Player position

        self.race_position_label_var = tk.StringVar(self.frame,
                                                    value=f'#{self.controller.get_position(self._racer.id)}')

        self.race_position_label = ttk.Label(self.frame, textvariable=self.race_position_label_var,
                                             font=('', 24, 'bold'))
        self.pack_widget(self.race_position_label, 'left', 2)

        # Player icon
        self.icon = tk.PhotoImage(file=PlayerRow.default_player_icon_path, width=50, height=50)
        self.icon_label = ttk.Label(self.frame, image=self.icon)
        self.pack_widget(self.icon_label, 'left', 2)

        # Player ID and display
        self._id_racer = self._racer.id
        self.racer_label = ttk.Label(self.frame, text=self.default_username+f'{self._id_racer}', font=('', 18))
        self.pack_widget(self.racer_label, 'left', 2)

        self.pack_frame()


if __name__ == '__main__':
    from view.MyTk import Window
    from model.MapViewModels import RaceModel
    from model.RaceClasses import Racer
    from controller.MapViewControllers import RaceController

    win = Window()
    my_racers = [Racer(33), Racer(14), Racer(1), Racer(66), Racer(84)]
    my_model = RaceModel()
    my_model.set_racers(my_racers)
    my_controller = RaceController(my_model)
    y = RacingRosterFrame(win, my_controller)
    win.mainloop()
