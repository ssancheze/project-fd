import typing


class BasicNavFrameModel:
    def __init__(self):
        self.right_callback = None
        self.left_callback = None
        self.left_callback = None

    def right_button_click(self):
        self.right_callback()

    def left_button_click(self):
        self.left_callback()

    def top_button_click(self):
        self.left_callback()

    def set_callback(self, value: str, func: typing.Callable):
        if value == 'right':
            self.right_callback = func
        elif value == 'left':
            self.left_callback = func
        elif value == 'top':
            self.left_callback = func


class WelcomeFrameModel(BasicNavFrameModel):
    def __init__(self):
        super().__init__()


class CreditsFrameModel(BasicNavFrameModel):
    def __init__(self):
        super().__init__()


class ModeSelectionFrameModel(BasicNavFrameModel):
    def __init__(self):
        super().__init__()
