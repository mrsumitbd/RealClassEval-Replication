from dataclasses import dataclass, field

@dataclass
class TaskDependency:
    layer_id: int
    task_id: int
    start_tiles: int
    end_tiles: int

    def __init__(self, layer_id=-1, task_id=-1, start_tiles=0, end_tiles=0):
        self.layer_id = layer_id
        self.task_id = task_id
        self.start_tiles = start_tiles
        self.end_tiles = end_tiles

    def cover(self, other):
        return other.layer_id == self.layer_id and other.task_id == self.task_id and (other.start_tiles >= self.start_tiles) and (other.end_tiles <= self.end_tiles)

    def to_empty(self):
        self.start_tiles = 0
        self.end_tiles = 0