
class Excels:
    '''
    Class to save the read Excel files and thus avoid double reading
    '''
    _files = {}
    _openpyxl_files = {}

    @classmethod
    def read(cls, file_name, tab):
        '''
        Read the Excel file or return the previously read one
        '''
        if file_name not in cls._files:
            import pandas as pd
            cls._files[file_name] = pd.read_excel(file_name, sheet_name=tab)
        return cls._files[file_name]

    @classmethod
    def read_opyxl(cls, file_name):
        '''
        Read the Excel file using OpenPyXL or return the previously read one
        '''
        if file_name not in cls._openpyxl_files:
            from openpyxl import load_workbook
            cls._openpyxl_files[file_name] = load_workbook(file_name)
        return cls._openpyxl_files[file_name]

    @classmethod
    def clean(cls):
        '''
        Clean the dictionary of read files
        '''
        cls._files.clear()
        cls._openpyxl_files.clear()
