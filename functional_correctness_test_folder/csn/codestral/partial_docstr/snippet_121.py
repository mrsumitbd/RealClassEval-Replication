
import pandas as pd
import openpyxl


class Excels:
    _read_files = {}

    @classmethod
    def read(cls, file_name, tab):
        if file_name not in cls._read_files:
            cls._read_files[file_name] = pd.read_excel(
                file_name, sheet_name=None)
        return cls._read_files[file_name][tab]

    @classmethod
    def read_opyxl(cls, file_name):
        if file_name not in cls._read_files:
            cls._read_files[file_name] = openpyxl.load_workbook(file_name)
        return cls._read_files[file_name]

    @classmethod
    def clean(cls):
        cls._read_files = {}
