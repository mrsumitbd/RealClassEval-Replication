import numpy as np
from openpyxl import load_workbook
import pandas as pd

class Excels:
    """
    Class to save the read Excel files and thus avoid double reading
    """
    _Excels, _Excels_opyxl = ({}, {})

    @classmethod
    def read(cls, file_name, tab):
        """
        Read the Excel file or return the previously read one
        """
        if file_name.joinpath(tab) in cls._Excels:
            return cls._Excels[file_name.joinpath(tab)]
        else:
            read_kwargs = {}
            ext = file_name.suffix.lower()
            if ext in _SPREADSHEET_EXTS:
                read_func = pd.read_excel
                read_kwargs['sheet_name'] = tab
            elif ext == '.csv':
                read_func = pd.read_csv
                if tab and (not tab[0].isalnum()):
                    read_kwargs['sep'] = tab
            else:
                read_func = pd.read_table
                if tab and (not tab[0].isalnum()):
                    read_kwargs['sep'] = tab
            excel = np.array([pd.to_numeric(ex, errors='coerce') for ex in read_func(file_name, header=None, **read_kwargs).values])
            cls._Excels[file_name.joinpath(tab)] = excel
            return excel

    @classmethod
    def read_opyxl(cls, file_name):
        """
        Read the Excel file using OpenPyXL or return the previously read one
        """
        if file_name in cls._Excels_opyxl:
            return cls._Excels_opyxl[file_name]
        else:
            excel = load_workbook(file_name, read_only=True, data_only=True)
            cls._Excels_opyxl[file_name] = excel
            return excel

    @classmethod
    def clean(cls):
        """
        Clean the dictionary of read files
        """
        for file in cls._Excels_opyxl.values():
            file.close()
        cls._Excels, cls._Excels_opyxl = ({}, {})