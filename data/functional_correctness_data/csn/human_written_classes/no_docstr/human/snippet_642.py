class Align:

    def __init__(self, seqrows, headers=None):
        self.rows = seqrows
        self.nrows = len(seqrows)
        ncol = None
        for rownum, row in enumerate(self.rows):
            try:
                if ncol is None:
                    ncol = len(row)
                elif ncol != len(row):
                    raise ValueError(f'Align: __init__:alignment block:row {rownum} does not have {ncol} columns, it has {len(row)}')
            except Exception:
                print(row)
                raise Exception('')
        self.ncols = ncol
        self.dims = (self.nrows, self.ncols)
        self.headers = headers

    def __str__(self):
        return '\n'.join(self.rows)