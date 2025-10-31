class Scorer:

    def __init__(self, match_cube=None):
        self.match_cube = match_cube

    def gap(self, x, y, parent):
        score_type = self.determine_type(x, y, parent)
        return Score(score_type, x, y, parent, parent.global_score - 1)

    def score(self, x, y, parent):
        rank = x - 1
        if self.match_cube.has_match(y - 1, rank):
            return Score(ScoreType.match, x, y, parent, parent.global_score + 1)
        return Score(ScoreType.mismatch, x, y, parent, parent.global_score - 1)

    @staticmethod
    def determine_type(x, y, parent):
        if x == parent.x:
            return ScoreType.addition
        if y == parent.y:
            return ScoreType.deletion
        return ScoreType.empty