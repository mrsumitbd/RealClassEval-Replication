import string

class ObjCentricEpisodicMemory:

    def __init__(self):
        self.reset()

    def get_objects(self, str):
        str_no_punc = str.translate(str.maketrans('', '', string.punctuation))
        words = str_no_punc.split()
        objects = []
        for i, w in enumerate(words):
            if w.isdigit() and i > 0:
                object = words[i - 1] + ' ' + w
                objects.append(object)
        return objects

    def push(self, stuff):
        assert len(stuff) > 0
        if len(self.memory) == 0:
            for _ in range(len(stuff)):
                self.memory.append(set())
        for b in range(len(stuff)):
            key = stuff[b]
            objects = self.get_objects(key)
            for obj in objects:
                self.memory[b].add(obj)

    def get_object_novelty_reward(self, stuff):
        assert len(stuff) > 0
        res = []
        for b in range(len(stuff)):
            key = stuff[b]
            objects = self.get_objects(key)
            if len(objects) > 0:
                num_unseen_objects = len([obj for obj in objects if obj not in self.memory[b]])
                res.append(float(num_unseen_objects) / len(objects))
            else:
                res.append(0.0)
        return res

    def reset(self):
        self.memory = []