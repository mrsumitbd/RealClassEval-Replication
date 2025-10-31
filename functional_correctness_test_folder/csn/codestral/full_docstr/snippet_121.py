
import openpyxl


class Excels:
    '''
    Class to save the read Excel files and thus avoid double reading
    '''
    _read_files = {}

    @classmethod
    def read(cls, file_name, tab):
        '''
        Read the Excel file or return the previously read one
        '''
        if file_name not in cls._read_files:
            cls._read_files[file_name] = {}
        if tab not in cls._read_files[file_name]:
            workbook = openpyxl.load_workbook(file_name)
            sheet = workbook[tab]
            cls._read_files[file_name][tab] = sheet
        return cls._read_files[file_name][tab]

    @classmethod
    def read_opyxl(cls, file_name):
        '''
        Read the Excel file using OpenPyXL or return the previously read one
        '''
        if file_name not in cls._read_files:
            workbook = openpyxl.load_workbook(file_name)
            cls._read_files[file_name] = workbook
        return cls._read_files[file_name]

    @classmethod
    def clean(cls):
        '''
        Clean the dictionary of read files
        '''
        cls._read_files = {}
