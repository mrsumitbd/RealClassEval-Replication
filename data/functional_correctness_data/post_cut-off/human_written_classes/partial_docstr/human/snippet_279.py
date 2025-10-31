import time
from typing import Optional, Dict, Any

class CycleDetail:
    """循环信息记录类"""

    def __init__(self, cycle_id: int):
        self.cycle_id = cycle_id
        self.thinking_id = ''
        self.start_time = time.time()
        self.end_time: Optional[float] = None
        self.timers: Dict[str, float] = {}
        self.loop_plan_info: Dict[str, Any] = {}
        self.loop_action_info: Dict[str, Any] = {}

    def to_dict(self) -> Dict[str, Any]:
        """将循环信息转换为字典格式"""

        def convert_to_serializable(obj, depth=0, seen=None):
            if seen is None:
                seen = set()
            if depth > 5:
                return str(obj)
            obj_id = id(obj)
            if obj_id in seen:
                return str(obj)
            seen.add(obj_id)
            try:
                if hasattr(obj, 'to_dict'):
                    return obj.to_dict()
                elif isinstance(obj, dict):
                    return {k: convert_to_serializable(v, depth + 1, seen) for k, v in obj.items() if isinstance(k, (str, int, float, bool))}
                elif isinstance(obj, (list, tuple)):
                    return [convert_to_serializable(item, depth + 1, seen) for item in obj if not isinstance(item, (dict, list, tuple)) or isinstance(item, (str, int, float, bool, type(None)))]
                elif isinstance(obj, (str, int, float, bool, type(None))):
                    return obj
                else:
                    return str(obj)
            finally:
                seen.remove(obj_id)
        return {'cycle_id': self.cycle_id, 'start_time': self.start_time, 'end_time': self.end_time, 'timers': self.timers, 'thinking_id': self.thinking_id, 'loop_plan_info': convert_to_serializable(self.loop_plan_info), 'loop_action_info': convert_to_serializable(self.loop_action_info)}

    def set_loop_info(self, loop_info: Dict[str, Any]):
        """设置循环信息"""
        self.loop_plan_info = loop_info['loop_plan_info']
        self.loop_action_info = loop_info['loop_action_info']