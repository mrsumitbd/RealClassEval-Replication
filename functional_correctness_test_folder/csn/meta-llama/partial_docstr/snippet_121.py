
import pandas as pd
from openpyxl import load_workbook


class Excels:
    _read_files = {}

    @classmethod
    def read(cls, file_name, tab):
        if file_name not in cls._read_files:
            cls._read_files[file_name] = {}
        if tab not in cls._read_files[file_name]:
            try:
                cls._read_files[file_name][tab] = pd.read_excel(
                    file_name, sheet_name=tab)
            except Exception as e:
                print(f"Failed to read {tab} from {file_name}: {str(e)}")
        return cls._read_files[file_name].get(tab)

    @classmethod
    def read_opyxl(cls, file_name):
        if file_name not in cls._read_files:
            cls._read_files[file_name] = {}
        if 'opyxl' not in cls._read_files[file_name]:
            try:
                cls._read_files[file_name]['opyxl'] = load_workbook(file_name)
            except Exception as e:
                print(f"Failed to read {file_name} using openpyxl: {str(e)}")
        return cls._read_files[file_name].get('opyxl')

    @classmethod
    def clean(cls):
        '''
        Clean the dictionary of read files
        '''
        cls._read_files.clear()
