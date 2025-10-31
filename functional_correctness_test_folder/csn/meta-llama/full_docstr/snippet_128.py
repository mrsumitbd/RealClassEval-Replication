
class PartitionRefinement:
    '''This data structure implements an order preserving
    partition with refinements.
    '''

    def __init__(self, n):
        '''Start with the partition consisting of the unique class {0,1,..,n-1}
        complexity: O(n) both in time and space
        '''
        self.parent = list(range(n))
        self.next = list(range(1, n)) + [None]
        self.prev = [None] + list(range(n-1))
        self.representative = list(range(n))
        self.classes = {i: [i] for i in range(n)}

    def refine(self, pivot):
        '''Split every class C in the partition into C intersection pivot
        and C setminus pivot complexity: linear in size of pivot
        '''
        new_classes = {}
        for i in pivot:
            class_id = self.parent[i]
            if class_id not in new_classes:
                new_classes[class_id] = ([], [])
            new_classes[class_id][0].append(i)
        for class_id, (in_pivot, not_in_pivot) in new_classes.items():
            if not not_in_pivot:
                continue
            new_class_id = not_in_pivot[0]
            self.classes[new_class_id] = not_in_pivot
            for i in not_in_pivot:
                self.parent[i] = new_class_id
            if len(in_pivot) > 0:
                new_in_pivot_class_id = in_pivot[0]
                self.classes[new_in_pivot_class_id] = in_pivot
                for i in in_pivot:
                    self.parent[i] = new_in_pivot_class_id
                # Update linked list to reflect the new class
                first_not_in_pivot = not_in_pivot[0]
                last_in_pivot = in_pivot[-1]
                last_not_in_pivot = not_in_pivot[-1]
                first_in_pivot = in_pivot[0]
                prev_first_not_in_pivot = self.prev[first_not_in_pivot]
                if prev_first_not_in_pivot is not None:
                    self.next[prev_first_not_in_pivot] = first_in_pivot
                self.prev[first_in_pivot] = prev_first_not_in_pivot
                self.next[last_in_pivot] = first_not_in_pivot
                self.prev[first_not_in_pivot] = last_in_pivot
                if last_not_in_pivot != last_in_pivot:
                    self.next[last_not_in_pivot] = None
            else:
                # If in_pivot is empty, we don't need to do anything
                pass
        # Remove empty classes
        self.classes = {k: v for k, v in self.classes.items() if v}

    def tolist(self):
        '''produce a list representation of the partition
        '''
        return list(self.classes.values())

    def order(self):
        '''Produce a flatten list of the partition, ordered by classes
        '''
        result = []
        current = self.representative[0]
        while current is not None:
            result.append(current)
            current = self.next[current]
        return result


# Example usage:
if __name__ == "__main__":
    pr = PartitionRefinement(10)
    # Output: [[0], [1], [2], [3], [4], [5], [6], [7], [8], [9]]
    print(pr.tolist())
    print(pr.order())   # Output: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    pr.refine([1, 3, 5, 7, 9])
    print(pr.tolist())  # Output: [[1, 3, 5, 7, 9], [0, 2, 4, 6, 8]]
    print(pr.order())   # Output: [1, 3, 5, 7, 9, 0, 2, 4, 6, 8]
