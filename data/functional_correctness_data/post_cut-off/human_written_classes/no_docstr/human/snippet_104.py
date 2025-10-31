from typing import Dict, Type, List, Any, Tuple, Union

class TaskIDManager:
    _type_id_counter: int = 0
    _type_id_map: Dict[Type, int] = {}
    _task_id_map: Dict[int, int] = {}

    @classmethod
    def get_task_type_id(cls, task_cls: Type) -> int:
        if task_cls not in cls._type_id_map:
            if cls._type_id_counter >= 2 ** 31 - 1:
                raise OverflowError('task_type_id exceeded int32 range')
            cls._type_id_map[task_cls] = cls._type_id_counter
            cls._type_id_counter += 1
        return cls._type_id_map[task_cls]

    @classmethod
    def get_task_id(cls, layer_id: int) -> int:
        current = cls._task_id_map.get(layer_id, 0)
        if current >= 2 ** 31 - 1:
            raise OverflowError(f'task_id exceeded int32 range for layer {layer_id}')
        cls._task_id_map[layer_id] = current + 1
        return current

    @classmethod
    def reset_task_ids(cls):
        cls._task_id_map.clear()

    @classmethod
    def reset_all_ids(cls):
        cls._type_id_counter = 0
        cls._type_id_map.clear()
        cls._task_id_map.clear()