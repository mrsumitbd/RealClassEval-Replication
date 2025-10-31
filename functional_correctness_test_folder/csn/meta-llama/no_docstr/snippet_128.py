
class PartitionRefinement:

    def __init__(self, n):
        self.partition = [{i} for i in range(n)]
        self.lookup = {i: i for i in range(n)}

    def refine(self, pivot):
        new_partition = []
        pivot_set = set(pivot)
        for subset in self.partition:
            intersection = subset & pivot_set
            difference = subset - pivot_set
            if intersection and difference:
                new_partition.append(intersection)
                new_partition.append(difference)
                for elem in intersection:
                    self.lookup[elem] = len(new_partition) - 2
                for elem in difference:
                    self.lookup[elem] = len(new_partition) - 1
            else:
                new_partition.append(subset)
                for elem in subset:
                    self.lookup[elem] = len(new_partition) - 1
        self.partition = new_partition

    def tolist(self):
        result = [-1] * len(self.lookup)
        for i, subset in enumerate(self.partition):
            for elem in subset:
                result[elem] = i
        return result

    def order(self):
        return sorted(range(len(self.lookup)), key=lambda x: self.lookup[x])
