import typing

import view.MyTk as MyTk
import tkinter.ttk as ttk
import tkinter.filedialog as tkfd


def _grid(tk_self, rows: int = None, cols: int = None):
    if rows is None and cols is None:
        return tk_self.grid_size()
    else:
        for rr in range(rows):
            tk_self.rowconfigure(rr, weight=1)
        for cc in range(cols):
            tk_self.columnconfigure(cc, weight=1)


def _text(tk_self, _text: str = None):
    if _text:
        tk_self.configure(text=_text)
    else:
        return tk_self.cget('text')


def _pack_widget(tk_self, side: str = None, padding: int = 0):
    if side is None:
        tk_self.pack(expand=True, fill='both')
    else:
        tk_self.pack(side=side, padx=padding, pady=padding)


class BasicFrame:
    def __init__(self, master=None, no_grid: bool = False, grid: typing.Tuple[int, int] = None,
                 navigation_buttons: bool = False, label: str = None):
        # General configuration
        self.master = master
        self.grid = _grid
        self.place_in_grid = MyTk.place_in_grid
        self.pack_widget = _pack_widget
        self.text = _text
        frame_init_kwargs = {}
        if label is not None:
            self.frame = ttk.LabelFrame
            frame_init_kwargs['text'] = label
        else:
            self.frame = ttk.Frame

        # master frame
        if master is not None:
            if isinstance(master, MyTk.Window):
                frame_init_kwargs['master'] = master.tk
            else:
                frame_init_kwargs['master'] = master

        self.frame = self.frame(**frame_init_kwargs)

        # Frame grid
        if not no_grid:
            if grid is None:
                self.grid(self.frame, 9, 16)
            else:
                self.grid(self.frame, *grid)

        # Navigation buttons
        if navigation_buttons:
            self.nav_buttons_frame = ttk.Frame(self.frame)
            # Right Button
            self.nav_right_button = ttk.Button(self.nav_buttons_frame, text='>')
            self.nav_right_button.pack(side='right', padx=10)

            # Left Button
            self.nav_left_button = ttk.Button(self.nav_buttons_frame, text='<')
            self.nav_left_button.pack(side='left', padx=10)

            # Center Button
            self.nav_center_button = ttk.Button(self.nav_buttons_frame, text='O')
            self.nav_center_button.pack(padx=10)
            self.place_in_grid(self.nav_buttons_frame, (8, 0), (8, 15))

    def pack_frame(self, **kwargs):
        if kwargs:
            self.frame.pack(**kwargs)
        else:
            self.frame.pack(expand=True, fill='both')


class RowFrameRow(BasicFrame):
    def __init__(self, master=None):
        super().__init__(master, no_grid=True)

        self.frame.configure(relief='groove', borderwidth=3)


class RowFrame(BasicFrame):
    def __init__(self, master=None, rows=1, label: str = None):
        super().__init__(master, no_grid=True, label=label)

        self.rows = rows
        self._options_rows_list: typing.List[RowFrameRow] = list()

    @property
    def options_rows_list(self):
        return self._options_rows_list

    def add_options_row(self, mode_options_row: RowFrameRow):
        if len(self._options_rows_list) > self.rows:
            raise IndexError(f'self.options_rows_list try to exceed maximum length')
        else:
            self._options_rows_list.append(mode_options_row)

    def pack_rows(self):
        for row in self.options_rows_list:
            row.pack_frame(side='top', fill='x')


class FileDialogFrame:
    FILETYPE_ALL = ('All files', '*.*')
    FILETYPE_WAYPOINTS = ('Waypoint files', '*.waypoints')
    FILE_EXTENSION_WAYPOINTS = 'waypoints'

    def __init__(self, master=None):
        self.master = master
        self._open_filename: typing.Optional[str] = None
        self._save_filename: typing.Optional[str] = None

    @property
    def open_filename(self):
        return self._open_filename

    @property
    def save_filename(self):
        return self._save_filename

    def ask_open_waypoints(self, open_dir: str):
        self._open_filename = tkfd.askopenfilename(parent=self.master,
                                                   filetypes=(self.FILETYPE_WAYPOINTS, self.FILETYPE_ALL),
                                                   initialdir=open_dir)

    def ask_save_waypoints(self, save_dir: str):
        self._save_filename = tkfd.asksaveasfilename(parent=self.master,
                                                     filetypes=(self.FILETYPE_WAYPOINTS, self.FILETYPE_ALL),
                                                     initialdir=save_dir,
                                                     defaultextension=self.FILE_EXTENSION_WAYPOINTS)


if __name__ == '__main__':
    tk = MyTk.Window()
    tk.config()
    y = BasicFrame(tk, navigation_buttons=True)
    y.frame.pack(expand=True, fill='both')
    tk.mainloop()
