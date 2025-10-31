
import json
import os
import yaml


class Parser:
    '''Provide tools to parse files
    '''

    def load_from_file(self, file_path, format=None):
        '''Return dict from a file config
        '''
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        if format is None:
            _, ext = os.path.splitext(file_path)
            format = ext.lower()[1:]  # Remove the dot

        with open(file_path, 'r') as file:
            if format == 'json':
                return json.load(file)
            elif format in ('yaml', 'yml'):
                return yaml.safe_load(file)
            else:
                raise ValueError(f"Unsupported file format: {format}")

    def load_all_from_directory(self, directory_path):
        '''Return a list of dict from a directory containing files
        '''
        if not os.path.isdir(directory_path):
            raise NotADirectoryError(f"Directory not found: {directory_path}")

        result = []
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                try:
                    data = self.load_from_file(file_path)
                    result.append(data)
                except ValueError:
                    continue  # Skip unsupported formats
        return result
