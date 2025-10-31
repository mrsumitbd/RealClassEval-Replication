
import os
import json
import configparser
import yaml


class Parser:
    '''Provide tools to parse files
    '''

    def load_from_file(self, file_path, format=None):
        '''Return dict from a file config
        '''
        if format is None:
            _, ext = os.path.splitext(file_path)
            ext = ext.lower()
            if ext in ['.json']:
                format = 'json'
            elif ext in ['.yaml', '.yml']:
                format = 'yaml'
            elif ext in ['.ini', '.cfg']:
                format = 'ini'
            else:
                raise ValueError(f"Unknown file extension: {ext}")

        if format == 'json':
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        elif format == 'yaml':
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        elif format == 'ini':
            config = configparser.ConfigParser()
            config.read(file_path, encoding='utf-8')
            return {section: dict(config.items(section)) for section in config.sections()}
        else:
            raise ValueError(f"Unsupported format: {format}")

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
