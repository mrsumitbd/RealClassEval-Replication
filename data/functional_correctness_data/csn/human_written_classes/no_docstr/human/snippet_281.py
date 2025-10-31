class PatternFilterMixin:
    ignore_patterns = []

    def get_ignored_patterns(self):
        return list(set(self.ignore_patterns))

    def list(self, ignore_patterns):
        if ignore_patterns:
            ignore_patterns = ignore_patterns + self.get_ignored_patterns()
        return super().list(ignore_patterns)