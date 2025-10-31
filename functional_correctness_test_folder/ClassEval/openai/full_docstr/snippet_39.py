
import os
import pandas as pd


class ExcelProcessor:
    """
    This is a class for processing excel files, including reading and writing excel data,
    as well as processing specific operations and saving as a new excel file.
    """

    def __init__(self):
        pass

    def read_excel(self, file_name):
        """
        Reading data from Excel files
        :param file_name: str, Excel file name to read
        :return: list of data, Data in Excel
        """
        if not os.path.isfile(file_name):
            raise FileNotFoundError(f"File '{file_name}' does not exist.")
        try:
            df = pd.read_excel(file_name, header=0)
            # Convert DataFrame to list of tuples
            data = [tuple(df.columns.tolist())] + [tuple(row)
                                                   for row in df.values]
            return data
        except Exception as e:
            raise RuntimeError(f"Failed to read Excel file '{file_name}': {e}")

    def write_excel(self, data, file_name):
        """
        Write data to the specified Excel file
        :param data: list, Data to be written
        :param file_name: str, Excel file name to write to
        :return: 0 or 1, 1 represents successful writing, 0 represents failed writing
        >>> processor = ExcelProcessor()
        >>> new_data = [
        >>>     ('Name', 'Age', 'Country'),
        >>>     ('John', 25, 'USA'),
        >>>     ('Alice', 30, 'Canada'),
        >>>     ('Bob', 35, 'Australia'),
        >>>     ('Julia', 28, 'Germany')
        >>> ]
        >>> data = processor.write_excel(new_data, 'test_data.xlsx')
        """
        if not isinstance(data, list) or len(data) == 0:
            return 0
        header = data[0]
        rows = data[1:]
        try:
            df = pd.DataFrame(rows, columns=header)
            df.to_excel(file_name, index=False)
            return 1
        except Exception:
            return 0

    def process_excel_data(self, N, save_file_name):
        """
        Change the specified column in the Excel file to uppercase
        :param N: int, The serial number of the column that want to change
        :param save_file_name: str, source file name
        :return: (int, str), The former is the return value of write_excel, while the latter is the saved file name of the processed data
        >>> processor = ExcelProcessor()
        >>> success, output_file = processor.process_excel_data(1, 'test_data.xlsx')
        """
        if not os.path.isfile(save_file_name):
            raise FileNotFoundError(
                f"Source file '{save_file_name}' does not exist.")
        try:
            df = pd.read_excel(save_file_name, header=0)
            if N < 1 or N > len(df.columns):
                raise IndexError(
                    f"Column index {N} is out of bounds for the data.")
            col_name = df.columns[N - 1]
            df[col_name] = df[col_name].astype(str).str.upper()
            base, ext = os.path.splitext(save_file_name)
            new_file_name = f"{base}_processed{ext}"
            df.to_excel(new_file_name, index=False)
            return 1, new_file_name
        except Exception:
            return 0, ""
