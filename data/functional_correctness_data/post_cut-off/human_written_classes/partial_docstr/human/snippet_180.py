from zsim.sim_progress.Character import Character, character_factory
from zsim.sim_progress.Buff import Buff
from dataclasses import dataclass, field
from zsim.sim_progress.Enemy import Enemy

@dataclass
class ScheduleData:
    enemy: Enemy
    char_obj_list: list[Character]
    event_list: list = field(default_factory=list)
    loading_buff: dict[str, list[Buff]] = field(default_factory=dict)
    dynamic_buff: dict[str, list[Buff]] = field(default_factory=dict)
    sim_instance: 'Simulator | None' = None
    processed_event: bool = False
    processed_times: int = field(default=0)
    processe_state_update_tick: int = field(default=0)

    def reset_myself(self):
        """重置ScheduleData的动态数据！"""
        self.enemy.reset_myself()
        self.event_list = []
        for char_name in self.loading_buff:
            self.loading_buff[char_name] = []
            self.dynamic_buff[char_name] = []
        self.processed_times = 0

    @property
    def processed_state_this_tick(self):
        """当前tick是否有新事件发生"""
        return self.processed_event

    def change_process_state(self):
        """有新事件发生时调用，保证终端print"""
        self.processed_event = True

    def reset_processed_event(self):
        """重置processed_event"""
        self.processed_event = False