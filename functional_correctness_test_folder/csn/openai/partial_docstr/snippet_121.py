
import pandas as pd
from openpyxl import load_workbook


class Excels:
    _files = {}

    @classmethod
    def read(cls, file_name, tab):
        """
        Read an Excel file and return the DataFrame for the specified sheet.
        The file is cached after the first read.
        """
        if file_name not in cls._files:
            # Load all sheets into a dict of DataFrames
            cls._files[file_name] = pd.read_excel(file_name, sheet_name=None)
        sheets = cls._files[file_name]
        if tab not in sheets:
            raise KeyError(f"Sheet '{tab}' not found in '{file_name}'.")
        return sheets[tab]

    @classmethod
    def read_opyxl(cls, file_name):
        """
        Read an Excel file using openpyxl and cache the workbook.
        """
        if file_name not in cls._files:
            cls._files[file_name] = load_workbook(file_name)
        return cls._files[file_name]

    @classmethod
    def clean(cls):
        """
        Clean the dictionary of read files.
        """
        cls._files.clear()
