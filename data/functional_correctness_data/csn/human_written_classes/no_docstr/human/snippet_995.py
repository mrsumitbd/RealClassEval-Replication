from performance.dynamicmodel import create_dict

class FastDynamicModelPerformance:

    def __init__(self, depth=5, children_count=5):
        self.depth = depth
        self.children_count = children_count

    def prepare(self):
        self.data = create_dict(self.depth, self.children_count)

    def run(self):
        return FakeDynModel(data={'fake_data': self.data})