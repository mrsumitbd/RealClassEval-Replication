
import os
import json
import yaml


class Parser:

    def load_from_file(self, file_path, format=None):
        if format is None:
            format = file_path.split('.')[-1]

        if format == 'json':
            with open(file_path, 'r') as file:
                return json.load(file)
        elif format == 'yaml' or format == 'yml':
            with open(file_path, 'r') as file:
                return yaml.safe_load(file)
        else:
            raise ValueError(f"Unsupported file format: {format}")

    def load_all_from_directory(self, directory_path):
        data_list = []
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                try:
                    data = self.load_from_file(file_path)
                    data_list.append(data)
                except ValueError as e:
                    print(f"Skipping {filename}: {e}")
        return data_list
