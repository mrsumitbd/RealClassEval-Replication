class ProductEntry:

    def __init__(self, name, mode, field, alias=None):
        self.name = name
        self.mode = mode
        self.field = field
        if alias is None:
            split_name = name.split('.')
            self.alias = split_name[-1]
        else:
            self.alias = alias

    def __repr__(self):
        msg = 'ProductEntry(name="{}", mode="{}", field="{}")'.format(self.name, self.mode, self.field)
        return msg