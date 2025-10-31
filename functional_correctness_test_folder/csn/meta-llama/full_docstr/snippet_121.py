
from openpyxl import load_workbook
import pandas as pd


class Excels:
    '''
    Class to save the read Excel files and thus avoid double reading
    '''
    _read_files = {}
    _read_opyxl_files = {}

    @classmethod
    def read(cls, file_name, tab):
        '''
        Read the Excel file or return the previously read one
        '''
        if file_name not in cls._read_files:
            cls._read_files[file_name] = {}
        if tab not in cls._read_files[file_name]:
            try:
                cls._read_files[file_name][tab] = pd.read_excel(
                    file_name, sheet_name=tab)
            except Exception as e:
                raise Exception(
                    f"Failed to read {tab} from {file_name}: {str(e)}")
        return cls._read_files[file_name][tab]

    @classmethod
    def read_opyxl(cls, file_name):
        '''
        Read the Excel file using OpenPyXL or return the previously read one
        '''
        if file_name not in cls._read_opyxl_files:
            try:
                cls._read_opyxl_files[file_name] = load_workbook(
                    filename=file_name, data_only=True)
            except Exception as e:
                raise Exception(
                    f"Failed to read {file_name} using OpenPyXL: {str(e)}")
        return cls._read_opyxl_files[file_name]

    @classmethod
    def clean(cls):
        '''
        Clean the dictionary of read files
        '''
        cls._read_files = {}
        cls._read_opyxl_files = {}
