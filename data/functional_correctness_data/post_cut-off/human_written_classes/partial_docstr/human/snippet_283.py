from collections import defaultdict

class LogIndex:
    """日志索引，用于快速检索和过滤"""

    def __init__(self):
        self.entries = []
        self.module_index = defaultdict(list)
        self.level_index = defaultdict(list)
        self.filtered_indices = []
        self.total_entries = 0

    def add_entry(self, index, entry):
        """添加日志条目到索引"""
        if index >= len(self.entries):
            self.entries.extend([None] * (index - len(self.entries) + 1))
        self.entries[index] = entry
        self.total_entries = max(self.total_entries, index + 1)
        logger_name = entry.get('logger_name', '')
        level = entry.get('level', '')
        self.module_index[logger_name].append(index)
        self.level_index[level].append(index)

    def filter_entries(self, modules=None, level=None, search_text=None):
        """根据条件过滤日志条目"""
        if not modules and (not level) and (not search_text):
            self.filtered_indices = list(range(self.total_entries))
            return self.filtered_indices
        candidate_indices = set(range(self.total_entries))
        if modules and '全部' not in modules:
            module_indices = set()
            for module in modules:
                module_indices.update(self.module_index.get(module, []))
            candidate_indices &= module_indices
        if level and level != '全部':
            level_indices = set(self.level_index.get(level, []))
            candidate_indices &= level_indices
        if search_text:
            search_text = search_text.lower()
            text_indices = set()
            for i in candidate_indices:
                if i < len(self.entries) and self.entries[i]:
                    entry = self.entries[i]
                    text_content = f"{entry.get('logger_name', '')} {entry.get('event', '')}".lower()
                    if search_text in text_content:
                        text_indices.add(i)
            candidate_indices &= text_indices
        self.filtered_indices = sorted(list(candidate_indices))
        return self.filtered_indices

    def get_filtered_count(self):
        """获取过滤后的条目数量"""
        return len(self.filtered_indices)

    def get_entry_at_filtered_position(self, position):
        """获取过滤结果中指定位置的条目"""
        if 0 <= position < len(self.filtered_indices):
            index = self.filtered_indices[position]
            return self.entries[index] if index < len(self.entries) else None
        return None