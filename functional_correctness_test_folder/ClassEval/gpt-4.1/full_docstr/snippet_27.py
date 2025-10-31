
import csv
import os


class CSVProcessor:
    """
    This is a class for processing CSV files, including reading and writing CSV data, as well as processing specific operations and saving as a new CSV file.
    """

    def __init__(self):
        pass

    def read_csv(self, file_name):
        """
        Read the csv file by file_name, get the title and data from it
        :param file_name: str, name of the csv file
        :return title, data: (list, list), first row is title, the rest is data
        """
        with open(file_name, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            if not rows:
                return [], []
            title = rows[0]
            data = rows[1:]
            return title, data

    def write_csv(self, data, file_name):
        """
        Write data into a csv file.
        :param file_name: str, name of the csv file
        :return:int, if success return 1, or 0 otherwise
        """
        try:
            with open(file_name, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for row in data:
                    writer.writerow(row)
            return 1
        except Exception:
            return 0

    def process_csv_data(self, N, save_file_name):
        """
        Read a csv file into variable title and data.
        Only remain the N th (from 0) column data and Capitalize them, store the title and new data into a new csv file.
        Add '_process' suffix after old file name, as a new file name.
        :param N: int, the N th column(from 0)
        :param save_file_name, the name of file that needs to be processed.
        :return:int, if success return 1, or 0 otherwise
        """
        try:
            title, data = self.read_csv(save_file_name)
            if not title or N < 0 or N >= len(title):
                return 0
            new_data = []
            for row in data:
                if len(row) > N:
                    new_data.append([row[N].upper()])
                else:
                    new_data.append([''])
            # Compose new file name
            base, ext = os.path.splitext(save_file_name)
            new_file_name = f"{base}_process{ext}"
            # Write new data: title row is the original title, but data is only Nth column
            out_data = [title] + new_data
            return self.write_csv(out_data, new_file_name)
        except Exception:
            return 0
