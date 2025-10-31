class TraversedDecisionTree:

    def __init__(self, tree):
        self.tree = tree
        self.branch_lengths = []
        self.positions = []
        self.adjacencies = [(left, right) for left, right in zip(self.tree.tree.children_left, self.tree.tree.children_right)]
        self.level_sizes = [0] * self.tree.tree_height
        self._traverse_tree(0, 0, 0, 0)

    def _traverse_tree(self, curr_node, curr_position, curr_level, curr_branch_length):
        self.level_sizes[curr_level] += 1
        if self.adjacencies[curr_node][0] == self.adjacencies[curr_node][1]:
            self.positions.append(curr_position)
            self.branch_lengths.append(curr_branch_length)
        else:
            self._traverse_tree(self.adjacencies[curr_node][0], curr_position - 1, curr_level + 1, curr_branch_length + 1)
            self._traverse_tree(self.adjacencies[curr_node][1], curr_position + 1, curr_level + 1, curr_branch_length + 1)

    def get_width(self):
        return abs(min(self.positions)) + abs(max(self.positions))