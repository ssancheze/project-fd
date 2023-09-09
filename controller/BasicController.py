

class BasicController:
    def __init__(self):
        """
        Base class for controllers. Accepts a BasicModel or subclass instance.
        """
        self._model = None

    @property
    def model(self):
        return self._model
