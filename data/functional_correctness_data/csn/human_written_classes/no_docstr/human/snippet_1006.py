class AbstractChoicesEnum:

    def __init__(self, *items):
        enum_items = []
        for item in items:
            assert len(item) in {2, 3}, 'Choice item array length must be two or three'
            if len(item) == 3:
                enum_items.append((item[0], item[2]))
            else:
                enum_items.append(item[0])
        super().__init__(*enum_items)
        self.choices = tuple(((k, items[i][1]) for i, k in enumerate(self._container.values())))

    def _get_labels_dict(self):
        return dict(self.choices)

    def get_label(self, name):
        labels = self._get_labels_dict()
        if name in labels:
            return labels[name]
        raise AttributeError('Missing label with index %s' % name)