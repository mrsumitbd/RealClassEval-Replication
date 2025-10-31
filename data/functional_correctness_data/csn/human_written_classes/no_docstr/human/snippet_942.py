from collections import Counter
from sklearn.tree import DecisionTreeClassifier

class DecisionTree:

    def __init__(self, X, Y, seed):
        self.tree = self._get_decision_tree(X, Y, seed)
        self.n_nodes = self.tree.node_count
        self.tree_height = self.tree.max_depth + 1
        self.leaf_count = Counter(self.tree.feature)[-2]

    def _get_decision_tree(self, X, Y, seed):
        estimator = DecisionTreeClassifier(random_state=seed)
        estimator.fit(X, Y)
        return estimator.tree_

    def get_general_info(self):
        return (self.n_nodes, self.leaf_count, self.tree_height)

    def get_attributes(self):
        return [x for x in Counter(self.tree.feature).values() if x != -2]