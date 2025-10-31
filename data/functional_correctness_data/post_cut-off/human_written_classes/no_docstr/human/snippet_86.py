class MemoryTracker:

    def __init__(self, name: str):
        self.name = name
        self.start_mem = get_memory_usage()
        self.stages = []

    def checkpoint(self, stage: str):
        current_mem = print_memory_stats(f'{self.name} - {stage}', self.start_mem)
        self.stages.append((stage, current_mem))
        return current_mem

    def summary(self):
        print(f'\n=== {self.name} Memory Summary ===')
        for stage, mem in self.stages:
            print(f'{stage}: {mem:.1f} MB')
        peak_mem = max((mem for _, mem in self.stages))
        print(f'Peak Memory: {peak_mem:.1f} MB')
        print(f'Total Memory Increase: {peak_mem - self.start_mem:.1f} MB')
        return peak_mem