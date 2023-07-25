import tkinter as tk
import view.WindowConfigMethods as WindowConfigMethods
import config
import typing


def place_in_grid(tk_self, top_left: typing.Tuple[int, int], bottom_right: typing.Tuple[int, int] = None,
                  padding: int = 0):
    if not bottom_right:
        bottom_right = top_left
    x0 = top_left[0]
    y0 = top_left[1]
    x1 = bottom_right[0]
    y1 = bottom_right[1]
    rowspan = x1 - x0 + 1
    columnspan = y1 - y0 + 1
    if padding < 5:
        padding = 5
    tk_self.grid(row=x0, column=y0, rowspan=rowspan, columnspan=columnspan, padx=padding, pady=padding, sticky='nsew')


class Window:
    """
    tkinter-based window class that is either a tkinter.Tk or tkinter.TopLevel based on whether it has an associated
    parent.
    """
    def __init__(self, master: tk.Misc = None):
        if not master:
            _tk = tk.Tk()
        else:
            _tk = tk.Toplevel(master)
        self.tk = _tk

    def config(self):
        """
        Configures the window's properties according to the file 'config.py'
        :return: None
        """
        config_keys = [key for key in config.__dict__ if '__' not in key and 'win_' in key]
        for key in config_keys:
            method = getattr(WindowConfigMethods, key)
            value = getattr(config, key)
            method(self, value)

    def mainloop(self):
        self.tk.mainloop()
