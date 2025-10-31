
import openpyxl
from typing import Dict, Any


class Excels:
    """
    Class to save the read Excel files and thus avoid double reading.
    """
    # Class-level cache: file_name -> workbook
    _cache: Dict[str, openpyxl.workbook.workbook.Workbook] = {}

    @classmethod
    def read(cls, file_name: str, tab: str) -> Any:
        """
        Read the Excel file or return the previously read one.
        Returns the worksheet object corresponding to the given tab.
        """
        wb = cls.read_opyxl(file_name)
        if tab not in wb.sheetnames:
            raise KeyError(f"Tab '{tab}' not found in workbook '{file_name}'.")
        return wb[tab]

    @classmethod
    def read_opyxl(cls, file_name: str) -> openpyxl.workbook.workbook.Workbook:
        """
        Read the Excel file using OpenPyXL or return the previously read one.
        """
        if file_name not in cls._cache:
            try:
                wb = openpyxl.load_workbook(file_name, data_only=True)
            except Exception as exc:
                raise IOError(
                    f"Failed to load workbook '{file_name}': {exc}") from exc
            cls._cache[file_name] = wb
        return cls._cache[file_name]

    @classmethod
    def clean(cls) -> None:
        """
        Clean the dictionary of read files.
        """
        cls._cache.clear()
