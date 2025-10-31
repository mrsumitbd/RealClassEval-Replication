import copy
import time
import json

class BufferQueue:

    def __init__(self, group_size, task_type='math', transform_group_func=None, is_valid_group_func=None, get_group_data_meta_info_func=None):
        self.data = {}
        self.temp_data = {}
        self.group_timestamps = {}
        self.group_size = group_size
        self.task_type = task_type
        self.is_valid_group_func = is_valid_group_func or default_is_valid_group
        self.get_group_data_meta_info_func = get_group_data_meta_info_func or default_get_group_data_meta_info
        self.transform_group_func = transform_group_func or (lambda group, task_type: group)

    def append(self, item):
        instance_id = item['instance_id']
        current_time = time.time()
        self.group_timestamps[instance_id] = current_time
        if instance_id not in self.temp_data:
            self.temp_data[instance_id] = [copy.deepcopy(item)]
        else:
            self.temp_data[instance_id].append(copy.deepcopy(item))
        if instance_id not in self.data:
            self.data[instance_id] = [item]
        else:
            self.data[instance_id].append(item)

    def _get_valid_groups_with_timeout(self, del_data=False):
        """Get valid groups including timeout-based groups"""
        valid_groups = {}
        timed_out_groups = {}
        finished_groups = []
        for instance_id, group_data in self.data.items():
            if self.is_valid_group_func((instance_id, group_data), self.group_size, self.task_type):
                valid_groups[instance_id] = group_data
        if del_data:
            for instance_id in finished_groups:
                self.data.pop(instance_id, None)
                self.group_timestamps.pop(instance_id, None)
                print(f'Removed finished group {instance_id}')
        all_valid_groups = {**valid_groups, **timed_out_groups}
        return (all_valid_groups, finished_groups)

    def get(self):
        output = {'data': [], 'meta_info': {}}
        meta_info = self.get_group_data_meta_info_func(self.temp_data)
        output['meta_info'] = meta_info
        valid_groups, finished_groups = self._get_valid_groups_with_timeout(del_data=True)
        output['meta_info']['finished_groups'] = finished_groups
        print(f'meta info: {json.dumps(meta_info, indent=2)}')
        valid_groups = list(valid_groups.items())
        for instance_id, group in valid_groups:
            transformed_group = self.transform_group_func((instance_id, group), self.task_type)
            output['data'].extend(transformed_group[1])
            if instance_id in self.data:
                self.data.pop(instance_id)
        return output

    def __len__(self):
        valid_groups, _ = self._get_valid_groups_with_timeout()
        num = sum([len(v) for v in valid_groups.values()])
        num_of_all_groups = sum([len(v) for v in self.data.values()])
        print(f'valid_groups: {len(valid_groups)}, num: {num}, num_of_all_groups: {num_of_all_groups}')
        return num