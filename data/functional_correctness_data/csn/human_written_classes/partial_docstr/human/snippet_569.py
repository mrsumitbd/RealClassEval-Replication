class TagRef:
    """
    Used when an ID in Stone refers to a tag of a union.
    TODO(kelkabany): Support tag values.
    """

    def __init__(self, union_data_type, tag_name):
        self.union_data_type = union_data_type
        self.tag_name = tag_name

    def __repr__(self):
        return 'TagRef({!r}, {!r})'.format(self.union_data_type, self.tag_name)