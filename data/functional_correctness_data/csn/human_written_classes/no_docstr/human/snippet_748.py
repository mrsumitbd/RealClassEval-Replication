class rectangular_block:

    def __init__(self):
        self.upper_row = 0
        self.lower_row = 0
        self.left_col = 0
        self.right_col = 0

    def __str__(self):
        attrs = vars(self)
        return ', '.join(('%s: %s' % item for item in attrs.items()))