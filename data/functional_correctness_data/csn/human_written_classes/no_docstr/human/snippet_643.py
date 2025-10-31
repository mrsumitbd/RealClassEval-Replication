from numpy import float32, putmask, shape, zeros

class AlignScoreMatrix:

    def __init__(self, align):
        nan = float('nan')
        matrix = zeros((align.nrows, align.ncols), float32)
        for ir in range(len(matrix)):
            for ic in range(len(matrix[ir])):
                matrix[ir][ic] = nan
        self.matrix = matrix

    def __len__(self):
        return shape(self.matrix)[1]

    def __str__(self):
        print(self.matrix)