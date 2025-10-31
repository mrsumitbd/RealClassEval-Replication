
import pandas as pd
from openpyxl import load_workbook


class Excels:
    _data = {}

    @classmethod
    def read(cls, file_name, tab):
        """Read Excel file into a pandas DataFrame"""
        try:
            cls._data[tab] = pd.read_excel(file_name, sheet_name=tab)
            return cls._data[tab]
        except Exception as e:
            print(f"Error reading file: {e}")
            return None

    @classmethod
    def read_opyxl(cls, file_name):
        """Read Excel file using openpyxl"""
        try:
            wb = load_workbook(filename=file_name)
            cls._data = {sheet.title: sheet for sheet in wb.worksheets}
            return cls._data
        except Exception as e:
            print(f"Error reading file: {e}")
            return None

    @classmethod
    def clean(cls):
        """Clear stored data"""
        cls._data = {}
