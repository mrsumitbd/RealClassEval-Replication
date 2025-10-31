from dataclasses import dataclass, field
from zsim.sim_progress.Buff import Buff

@dataclass
class GlobalStats:
    name_box: list
    DYNAMIC_BUFF_DICT: dict[str, list[Buff]] = field(default_factory=dict)
    sim_instance: 'Simulator | None' = None

    def __post_init__(self):
        for name in self.name_box + ['enemy']:
            self.DYNAMIC_BUFF_DICT[name] = []

    def reset_myself(self, name_box):
        for name in self.name_box + ['enemy']:
            self.DYNAMIC_BUFF_DICT[name] = []