import typing
from os.path import join

from model.MapViewModels import RaceModel
from definitions import FENCES_DIR


class TrackManager:
    def __init__(self):
        self._track_name: typing.Optional[str] = None

        self._race_model: typing.Optional[RaceModel] = None

    @property
    def race_model(self):
        return self._race_model

    def select_track(self, track_name: str):
        self._track_name = join(FENCES_DIR, track_name)

        self._race_model = RaceModel()
        self._race_model.open_map_from_file(self._track_name)
        self._race_model.create_checkpoints()

    def clear_track(self):
        self._track_name = None
        self._race_model = None


if __name__ == '__main__':
    pass
