class StringTableOptimiser:
    """
    Optimizes the order of keys and values in the MVT layer string table.

    Counts the number of times an entry in the MVT string table (both keys and values) is used. Then reorders the
    string table to have the most commonly used entries first and updates the features to use the replacement
    locations in the table. This can save several percent in a tile with large numbers of features.
    """

    def __init__(self):
        self.key_counts = {}
        self.val_counts = {}

    def add_tags(self, feature_tags):
        itr = iter(feature_tags)
        for k, v in zip(itr, itr):
            self.key_counts[k] = self.key_counts.get(k, 0) + 1
            self.val_counts[v] = self.val_counts.get(v, 0) + 1

    @staticmethod
    def _update_table(counts, table):
        sort = sorted(((c, k) for k, c in counts.items()), reverse=True)
        new_table = []
        for _, x in sort:
            new_table.append(table[x])
        assert len(new_table) == len(table)
        del table[:]
        table.extend(new_table)
        new_indexes = {}
        for i, (_, k) in enumerate(sort):
            new_indexes[k] = i
        return new_indexes

    def update_string_table(self, layer):
        new_key = self._update_table(self.key_counts, layer.keys)
        new_val = self._update_table(self.val_counts, layer.values)
        for feature in layer.features:
            for i in range(0, len(feature.tags), 2):
                feature.tags[i] = new_key[feature.tags[i]]
                feature.tags[i + 1] = new_val[feature.tags[i + 1]]