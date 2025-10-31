class MemoryTracker:

    def __init__(self, name: str):
        self.name = name
        self.start_mem = get_memory_usage()
        self.stages = []

    def checkpoint(self, stage: str):
        current_mem = get_memory_usage()
        diff = current_mem - self.start_mem
        print(f'[{self.name} - {stage}] Memory: {current_mem:.1f} MB (+{diff:.1f} MB)')
        self.stages.append((stage, current_mem))
        return current_mem

    def summary(self):
        peak_mem = max((mem for _, mem in self.stages))
        print(f'Peak Memory: {peak_mem:.1f} MB')
        return peak_mem