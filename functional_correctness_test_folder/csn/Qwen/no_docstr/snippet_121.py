
import pandas as pd
from openpyxl import load_workbook


class Excels:

    @classmethod
    def read(cls, file_name, tab):
        return pd.read_excel(file_name, sheet_name=tab)

    @classmethod
    def read_opyxl(cls, file_name):
        workbook = load_workbook(filename=file_name)
        return workbook

    @classmethod
    def clean(cls):
        # Assuming cleaning involves resetting the class state or clearing cached data
        # Here, we do nothing as there's no state to clean in this simple implementation
        pass
