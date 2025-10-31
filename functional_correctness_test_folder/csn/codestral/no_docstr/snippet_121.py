
import pandas as pd
import openpyxl


class Excels:

    @classmethod
    def read(cls, file_name, tab):
        df = pd.read_excel(file_name, sheet_name=tab)
        return df

    @classmethod
    def read_opyxl(cls, file_name):
        wb = openpyxl.load_workbook(file_name)
        return wb

    @classmethod
    def clean(cls):
        pass
