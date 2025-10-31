
import pandas as pd
import openpyxl


class Excels:
    '''
    Class to save the read Excel files and thus avoid double reading
    '''
    _pandas_cache = {}
    _openpyxl_cache = {}

    @classmethod
    def read(cls, file_name, tab):
        '''
        Read the Excel file or return the previously read one
        '''
        key = (file_name, tab)
        if key not in cls._pandas_cache:
            df = pd.read_excel(file_name, sheet_name=tab)
            cls._pandas_cache[key] = df
        return cls._pandas_cache[key]

    @classmethod
    def read_opyxl(cls, file_name):
        '''
        Read the Excel file using OpenPyXL or return the previously read one
        '''
        if file_name not in cls._openpyxl_cache:
            wb = openpyxl.load_workbook(file_name)
            cls._openpyxl_cache[file_name] = wb
        return cls._openpyxl_cache[file_name]

    @classmethod
    def clean(cls):
        '''
        Clean the dictionary of read files
        '''
        cls._pandas_cache.clear()
        cls._openpyxl_cache.clear()
