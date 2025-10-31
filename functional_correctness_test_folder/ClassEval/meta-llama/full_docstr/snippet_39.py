
import pandas as pd


class ExcelProcessor:
    """
    This is a class for processing excel files, including reading and writing excel data, as well as processing specific operations and saving as a new excel file.
    """

    def __init__(self):
        pass

    def read_excel(self, file_name):
        """
        Reading data from Excel files
        :param file_name:str, Excel file name to read
        :return:list of data, Data in Excel
        """
        try:
            data = pd.read_excel(file_name, header=None).values.tolist()
            return data
        except Exception as e:
            print(f"Error reading Excel file: {e}")
            return []

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
        try:
            df = pd.DataFrame(data)
            df.to_excel(file_name, index=False, header=False)
            return 1
        except Exception as e:
            print(f"Error writing Excel file: {e}")
            return 0

    def process_excel_data(self, N, file_name):
        """
        Change the specified column in the Excel file to uppercase
        :param N: int, The serial number of the column that want to change
        :param file_name: str, source file name
        :return:(int, str), The former is the return value of write_excel, while the latter is the saved file name of the processed data
        >>> processor = ExcelProcessor()
        >>> success, output_file = processor.process_excel_data(1, 'test_data.xlsx')
        """
        data = self.read_excel(file_name)
        if not data:
            return 0, ""

        for i in range(len(data)):
            if N < len(data[i]):
                if isinstance(data[i][N], str):
                    data[i][N] = data[i][N].upper()

        save_file_name = f"processed_{file_name}"
        write_status = self.write_excel(data, save_file_name)
        return write_status, save_file_name


# Example usage:
if __name__ == "__main__":
    processor = ExcelProcessor()
    new_data = [
        ('Name', 'Age', 'Country'),
        ('John', 25, 'USA'),
        ('Alice', 30, 'Canada'),
        ('Bob', 35, 'Australia'),
        ('Julia', 28, 'Germany')
    ]
    processor.write_excel(new_data, 'test_data.xlsx')
    success, output_file = processor.process_excel_data(1, 'test_data.xlsx')
    print(f"Processing status: {success}, Output file: {output_file}")
