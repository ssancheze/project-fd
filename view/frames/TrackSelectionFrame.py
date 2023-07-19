from view.frames.BasicFrame import BasicFrame
import tkinter.ttk as ttk
import tkinter as tk


class TrackSelectionFrame(BasicFrame):
    def __init__(self, master=None):
        super().__init__(master, navigation_buttons=True)

        # Title Label
        self.title_label = ttk.Label(self.frame, text='SELECT\nTRACK', anchor=tk.CENTER, font=('', 21))
        self.place_in_grid(self.title_label, (0, 0), (3, 3))

        # Scrollbar frame (so that the method .pack can be applied to the widget without messing the grid)
        self.scrollbar_frame_class = ScrollbarFrame(self.frame)
        self.place_in_grid(self.scrollbar_frame_class.frame, (0, 4), (7, 15))


class ScrollbarFrame(BasicFrame):
    def __init__(self, master=None):
        super().__init__(master, no_grid=True)

        # Scrollbar widget
        self.track_scrollbar = ttk.Scrollbar(self.frame, orient='vertical')
        self.track_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Track Frame
        self.track_frame = ttk.LabelFrame(self.frame, text='TRACKS')
        self.track_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5)


if __name__ == '__main__':
    import view.MyTk as MyTk
    win = MyTk.Window()
    win.config()
    TrackSelectionFrame(win).pack_frame()
    win.mainloop()
