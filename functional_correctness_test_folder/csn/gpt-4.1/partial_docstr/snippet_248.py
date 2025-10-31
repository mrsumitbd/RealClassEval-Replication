
import os
import json
import yaml


class Parser:

    def load_from_file(self, file_path, format=None):
        if format is None:
            _, ext = os.path.splitext(file_path)
            ext = ext.lower()
            if ext in ['.json']:
                format = 'json'
            elif ext in ['.yaml', '.yml']:
                format = 'yaml'
            else:
                raise ValueError(
                    "Unknown file format for file: {}".format(file_path))
        with open(file_path, 'r', encoding='utf-8') as f:
            if format == 'json':
                return json.load(f)
            elif format == 'yaml':
                return yaml.safe_load(f)
            else:
                raise ValueError("Unsupported format: {}".format(format))

    def load_all_from_directory(self, directory_path):
        '''Return a list of dict from a directory containing files
        '''
        result = []
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                try:
                    data = self.load_from_file(file_path)
                    result.append(data)
                except Exception:
                    continue
        return result
