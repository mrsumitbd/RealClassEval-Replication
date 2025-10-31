class ScoreIterator:

    def __init__(self, score_matrix):
        self.score_matrix = score_matrix
        self.x = len(score_matrix[0]) - 1
        self.y = len(score_matrix) - 1

    def __iter__(self):
        return self

    def _has_next(self):
        return not (self.x == 0 and self.y == 0)

    def __next__(self):
        if self._has_next():
            current_score = self.score_matrix[self.y][self.x]
            self.x = current_score.previous_x
            self.y = current_score.previous_y
            return current_score
        else:
            raise StopIteration()