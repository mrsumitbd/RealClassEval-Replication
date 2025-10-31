class Score:

    def __init__(self, score_type, x, y, parent, global_score=None):
        self.type = score_type
        self.x = x
        self.y = y
        self.parent = parent
        self.previous_x = 0 if parent is None else parent.x
        self.previous_y = 0 if parent is None else parent.y
        self.global_score = parent.global_score if global_score is None else global_score

    def __repr__(self):
        return str.format('({},{})', self.global_score, self.type.name)