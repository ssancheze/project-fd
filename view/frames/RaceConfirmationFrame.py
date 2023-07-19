from view.frames.BasicFrame import BasicFrame
import tkinter.ttk as ttk
import tkinter as tk


class RaceConfirmationFrame(BasicFrame):
    def __init__(self, master=None):
        super().__init__(master, navigation_buttons=True)

        # Title Label
        self.title_label = ttk.Label(self.frame, text='RACE\nSETTINGS', anchor=tk.CENTER, font=('', 21))
        self.place_in_grid(self.title_label, (0, 0), (0, 5))

        # Mode settings frame
        self.mode_settings_label = ttk.LabelFrame(self.frame, text='MODE SETTINGS')
        self.place_in_grid(self.mode_settings_label, (1, 0), (2, 5))

        # Drone list frame
        self.drone_list_frame = ttk.LabelFrame(self.frame, text='RACER(S)')
        self.place_in_grid(self.drone_list_frame, (3, 0), (7, 5))

        # Track frame
        self.track_frame = ttk.LabelFrame(self.frame, text='TRACK')
        self.place_in_grid(self.track_frame, (0, 6), (7, 15))


if __name__ == '__main__':
    import view.MyTk as MyTk
    win = MyTk.Window()
    win.config()
    RaceConfirmationFrame(win).pack_frame()
    win.mainloop()
