
import os
import pandas as pd
import openpyxl


class Excels:
    """
    Simple helper for reading Excel files with optional caching.
    """

    _cache = {}

    @classmethod
    def read(cls, file_name: str, tab: str):
        """
        Read a specific sheet from an Excel file and cache the result.

        Parameters
        ----------
        file_name : str
            Path to the Excel file.
        tab : str
            Sheet name to read.

        Returns
        -------
        pandas.DataFrame
            The contents of the requested sheet.
        """
        key = (os.path.abspath(file_name), tab)
        if key not in cls._cache:
            cls._cache[key] = pd.read_excel(file_name, sheet_name=tab)
        return cls._cache[key]

    @classmethod
    def read_opyxl(cls, file_name: str):
        """
        Load an Excel workbook using openpyxl.

        Parameters
        ----------
        file_name : str
            Path to the Excel file.

        Returns
        -------
        openpyxl.workbook.workbook.Workbook
            The loaded workbook object.
        """
        return openpyxl.load_workbook(file_name)

    @classmethod
    def clean(cls):
        """
        Clear the internal cache of loaded sheets.
        """
        cls._cache.clear()
