class EpisodicCountingMemory:

    def __init__(self):
        self.reset()

    def push(self, stuff):
        assert len(stuff) > 0
        if len(self.memory) == 0:
            for _ in range(len(stuff)):
                self.memory.append(set())
        for b in range(len(stuff)):
            key = stuff[b]
            self.memory[b].add(key)

    def is_a_new_state(self, stuff):
        assert len(stuff) > 0
        res = []
        for b in range(len(stuff)):
            key = stuff[b]
            res.append(float(key not in self.memory[b]))
        return res

    def reset(self):
        self.memory = []

    def __len__(self):
        return len(self.memory)