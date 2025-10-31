import os
from opyplus.conf import CONF
import pandas as pd

class OutputTable:
    """
    Class describing an E+ output table.

    Parameters
    ----------
    path: str
        Path of the E+ output table file.
    """

    def __init__(self, path):
        if not os.path.isfile(path):
            raise FileNotFoundError("No file at given path: '%s'." % path)
        self._path = path
        self._reports_d = self._parse()

    def _parse(self):
        _name_ = 'name'
        _columns_ = 'columns'
        _values_ = 'values'
        _index_ = 'index'
        raw_reports_d = {}
        current_raw_tables_l = None
        current_raw_table_d = None
        columns_nb = None
        with open(self._path, 'r', encoding=CONF.encoding) as f:
            while True:
                try:
                    line_s = next(f).strip()
                except StopIteration:
                    break
                if line_s[:6] == 'REPORT':
                    report_name = line_s.split(',')[1].strip()
                    current_raw_tables_l = []
                    raw_reports_d[report_name] = current_raw_tables_l
                    current_raw_table_d = {_index_: [], _values_: []}
                    for i in range(2):
                        next(f)
                    continue
                elif current_raw_tables_l is None:
                    continue
                elif line_s[:5] == 'Note ':
                    break
                if line_s.strip() == '':
                    if _columns_ in current_raw_table_d:
                        current_raw_table_d = {_index_: [], _values_: []}
                elif _name_ not in current_raw_table_d:
                    current_raw_table_d[_name_] = line_s
                    current_raw_tables_l.append(current_raw_table_d)
                elif _columns_ not in current_raw_table_d:
                    columns_l = line_s.split(',')[2:]
                    current_raw_table_d[_columns_] = columns_l
                    columns_nb = len(columns_l)
                else:
                    line_l = line_s.split(',')
                    if len(line_l) <= 1:
                        continue
                    current_raw_table_d[_index_].append(','.join(line_l[1:-columns_nb]))
                    current_raw_table_d[_values_].append([to_float_if_possible(s) for s in line_l[-columns_nb:]])
        reports_d = {}
        for report_name, raw_tables_l in raw_reports_d.items():
            tables_d = {}
            for raw_table_d in raw_tables_l:
                tables_d[raw_table_d[_name_]] = pd.DataFrame(data=raw_table_d[_values_], index=raw_table_d[_index_], columns=raw_table_d[_columns_])
            reports_d[report_name] = tables_d
        return reports_d

    def get_table(self, table_name, report_name=None):
        """
        Get table.

        # TODO [GL]: fill docstring (including Returns section)

        Parameters
        ----------
        table_name: str
        report_name: str
        """
        if report_name is None:
            for rp_name, tables_d in self._reports_d.items():
                if table_name in tables_d:
                    return tables_d[table_name]
            raise KeyError("Table name '%s' not found." % table_name)
        if report_name not in self._reports_d:
            raise KeyError("Report name '%s' not found." % report_name)
        tables_d = self._reports_d[report_name]
        if table_name not in tables_d:
            raise KeyError("Table name '%s' not found in report '%s'." % (table_name, report_name))
        return tables_d[table_name]