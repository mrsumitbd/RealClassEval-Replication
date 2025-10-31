from dataclasses import asdict
from cellpy.parameters import prms

class DbSheetCols:

    def __init__(self):
        db_cols_from_prms = asdict(prms.DbCols)
        self.keys = []
        self.headers = []
        for table_key, value in db_cols_from_prms.items():
            if isinstance(value, (list, tuple)):
                value = value[0]
            setattr(self, table_key, value)
            self.keys.append(table_key)
            self.headers.append(value)

    def __repr__(self):
        return f'<DbCols: {self.__dict__}>'