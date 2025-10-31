
import pandas as pd
import openpyxl


class Excels:
    _files = {}

    @classmethod
    def read(cls, file_name, tab):
        """
        Reads an Excel file using pandas and stores the DataFrame in the class dictionary.
        """
        key = (file_name, tab)
        if key not in cls._files:
            df = pd.read_excel(file_name, sheet_name=tab)
            cls._files[key] = df
        return cls._files[key]

    @classmethod
    def read_opyxl(cls, file_name):
        """
        Reads an Excel file using openpyxl and stores the workbook in the class dictionary.
        """
        if file_name not in cls._files:
            wb = openpyxl.load_workbook(file_name)
            cls._files[file_name] = wb
        return cls._files[file_name]

    @classmethod
    def clean(cls):
        '''
        Clean the dictionary of read files
        '''
        cls._files.clear()
