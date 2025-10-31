
import os
import json
import csv


class Parser:

    def load_from_file(self, file_path, format=None):
        if format is None:
            _, ext = os.path.splitext(file_path)
            format = ext[1:].lower()

        if format == 'json':
            with open(file_path, 'r') as file:
                return json.load(file)
        elif format == 'csv':
            with open(file_path, 'r', newline='') as file:
                reader = csv.DictReader(file)
                return [row for row in reader]
        else:
            raise ValueError(f"Unsupported file format: {format}")

    def load_all_from_directory(self, directory_path):
        data = []
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                try:
                    file_data = self.load_from_file(file_path)
                    data.append(file_data)
                except ValueError as e:
                    print(f"Error loading {filename}: {e}")
        return data
