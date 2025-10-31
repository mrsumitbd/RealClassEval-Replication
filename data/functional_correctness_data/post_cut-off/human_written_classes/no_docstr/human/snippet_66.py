import threading

class RolloutBuffer:

    def __init__(self, group_size=16, task_type='math', transform_group_func=None, is_valid_group_func=None, get_group_data_meta_info_func=None):
        self.buffer = BufferQueue(group_size=group_size, task_type=task_type, transform_group_func=transform_group_func, is_valid_group_func=is_valid_group_func, get_group_data_meta_info_func=get_group_data_meta_info_func)
        self.lock = threading.RLock()
        self.not_empty = threading.Condition(self.lock)
        self.total_written = 0
        self.total_read = 0
        self.task_type = task_type

    def write(self, data):
        with self.lock:
            self.buffer.append(data)
            self.total_written += 1
            self.not_empty.notify_all()
        return data

    def read(self):
        with self.not_empty:
            if len(self.buffer) == 0:
                return {'data': [], 'meta_info': {}}
            result = self.buffer.get()
            self.total_read += len(result['data'])
            return result