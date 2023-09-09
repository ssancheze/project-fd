from model.FrameModels import BasicNavFrameModel, WelcomeFrameModel, CreditsFrameModel


class BasicNavFrameController:
    def __init__(self, model: BasicNavFrameModel):
        self._model = model

    def right_button_click(self):
        self._model.right_button_click()

    def top_button_click(self):
        self._model.top_button_click()

    def left_button_click(self):
        self._model.left_button_click()


class WelcomeFrameController(BasicNavFrameController):
    def __init__(self, model: WelcomeFrameModel):
        super().__init__(model)

    def right_button_click(self):
        pass

    def top_button_click(self):
        pass

    def left_button_click(self):
        pass


class CreditsFrameController(BasicNavFrameController):
    def __init__(self, model: CreditsFrameModel):
        super().__init__(model)

    def right_button_click(self):
        pass

    def top_button_click(self):
        pass

    def left_button_click(self):
        pass


class ModeSelectionFrameController(BasicNavFrameController):
    pass
