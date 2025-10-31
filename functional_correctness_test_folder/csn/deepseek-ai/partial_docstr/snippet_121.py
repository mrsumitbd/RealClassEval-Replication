
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
import pandas as pd


class Excels:
    _files = {}

    @classmethod
    def read(cls, file_name, tab):
        if file_name not in cls._files:
            cls._files[file_name] = pd.ExcelFile(file_name)
        return cls._files[file_name].parse(tab)

    @classmethod
    def read_opyxl(cls, file_name):
        if file_name not in cls._files:
            cls._files[file_name] = openpyxl.load_workbook(file_name)
        return cls._files[file_name]

    @classmethod
    def clean(cls):
        cls._files = {}
