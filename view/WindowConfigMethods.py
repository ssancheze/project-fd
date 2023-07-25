import typing


def win_windowed_resolution(self, dimensions: typing.Tuple[int, int]):
    self.tk.geometry(f'{dimensions[0]}x{dimensions[1]}')


def win_borderless(self, value: bool) -> None:
    self.tk.overrideredirect(value)


def win_resizable(self, option: str) -> None:
    if 'h' in option and 'v' in option:
        self.tk.resizable(True, True)
    elif 'h' in option:
        self.tk.resizable(True, False)
    elif 'v' in option:
        self.tk.resizable(False, True)
    else:
        self.tk.resizable(False, False)


def win_fullscreen(self, value: bool):
    def _toggle_fullscreen(event=None):
        self.state = not self.state  # Just toggling the boolean
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def _end_fullscreen(event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"

    if value:
        self.state = False
        self.tk.bind("<F11>", _toggle_fullscreen)
        self.tk.bind("<Escape>", _end_fullscreen)
