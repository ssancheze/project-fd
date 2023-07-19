import typing

import view.MyTk as MyTk
import tkinter.ttk as ttk


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


if __name__ == '__main__':
    tk = MyTk.Window()
    tk.config()
    y = BasicFrame(tk, navigation_buttons=True)
    y.frame.pack(expand=True, fill='both')
    tk.mainloop()
