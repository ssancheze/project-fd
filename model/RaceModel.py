from typing import Optional

from model.MapViewModels import FenceCheckpointModel
from model.utils import TrackLength, StartingPoints


class RaceModel(FenceCheckpointModel):
    def __init__(self):
        """
        Race handler
        """
        FenceCheckpointModel.__init__(self)

        self._track_length: Optional[TrackLength] = None
        self._starting_points: Optional[StartingPoints] = None

    @property
    def starting_points(self):
        return self._starting_points

    def create_track_length(self):
        self._track_length = TrackLength(self.checkpoints)

    def create_starting_points(self, player_count: int):
        self._starting_points = StartingPoints(self._track_length, player_count)


if __name__ == '__main__':
    pass
