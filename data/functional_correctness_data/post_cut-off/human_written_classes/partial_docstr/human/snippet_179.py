from zsim.sim_progress.Buff.Buff0Manager import Buff0ManagerClass, change_name_box
from dataclasses import dataclass, field
from zsim.sim_progress.data_struct import ActionStack

@dataclass
class LoadData:
    name_box: list
    Judge_list_set: list
    weapon_dict: dict
    action_stack: ActionStack
    cinema_dict: dict
    exist_buff_dict: dict = field(init=False)
    load_mission_dict: dict = field(default_factory=dict)
    LOADING_BUFF_DICT: dict = field(default_factory=dict)
    name_dict: dict = field(default_factory=dict)
    all_name_order_box: dict = field(default_factory=dict)
    preload_tick_stamp: dict = field(default_factory=dict)
    char_obj_dict: dict | None = None
    sim_instance: 'Simulator | None' = None

    def __post_init__(self):
        self.buff_0_manager = Buff0ManagerClass.Buff0Manager(self.name_box, self.Judge_list_set, self.weapon_dict, self.cinema_dict, self.char_obj_dict, sim_instance=self.sim_instance)
        self.exist_buff_dict = self.buff_0_manager.exist_buff_dict
        self.all_name_order_box = change_name_box(self.name_box)

    def reset_exist_buff_dict(self):
        """重置buff_exist_dict"""
        for char_name, sub_exist_buff_dict in self.exist_buff_dict.items():
            for buff_name, buff in sub_exist_buff_dict.items():
                buff.reset_myself()

    def reset_myself(self, name_box, Judge_list_set, weapon_dict, cinema_dict):
        self.name_box = name_box
        self.Judge_list_set = Judge_list_set
        self.weapon_dict = weapon_dict
        self.cinema_dict = cinema_dict
        self.action_stack.reset_myself()
        self.reset_exist_buff_dict()
        self.load_mission_dict = {}
        self.LOADING_BUFF_DICT = {}
        self.name_dict = {}
        self.all_name_order_box = change_name_box(self.name_box)
        self.preload_tick_stamp = {}