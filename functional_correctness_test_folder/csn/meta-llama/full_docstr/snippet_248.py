
import os
import json
import yaml


class Parser:
    '''Provide tools to parse files
    '''

    def load_from_file(self, file_path, format=None):
        '''Return dict from a file config
        '''
        if format is None:
            _, file_extension = os.path.splitext(file_path)
            format = file_extension[1:].lower()

        if format == 'json':
            with open(file_path, 'r') as file:
                return json.load(file)
        elif format == 'yaml' or format == 'yml':
            with open(file_path, 'r') as file:
                return yaml.safe_load(file)
        else:
            raise ValueError(f"Unsupported file format: {format}")

    def load_all_from_directory(self, directory_path):
        '''Return a list of dict from a directory containing files
        '''
        result = []
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                try:
                    result.append(self.load_from_file(file_path))
                except ValueError as e:
                    print(f"Skipping file {filename}: {e}")
        return result
