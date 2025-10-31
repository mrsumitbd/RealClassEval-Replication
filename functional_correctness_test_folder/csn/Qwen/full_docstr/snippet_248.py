
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
            _, ext = os.path.splitext(file_path)
            format = ext[1:].lower()

        with open(file_path, 'r') as file:
            if format == 'json':
                return json.load(file)
            elif format == 'yaml' or format == 'yml':
                return yaml.safe_load(file)
            else:
                raise ValueError(f"Unsupported file format: {format}")

    def load_all_from_directory(self, directory_path):
        '''Return a list of dict from a directory containing files
        '''
        configs = []
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                try:
                    config = self.load_from_file(file_path)
                    configs.append(config)
                except ValueError as e:
                    print(f"Error loading {file_path}: {e}")
        return configs
