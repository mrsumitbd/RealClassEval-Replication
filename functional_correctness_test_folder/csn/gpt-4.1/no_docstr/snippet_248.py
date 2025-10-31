
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
                    "Unknown file format and no format specified.")
        with open(file_path, 'r', encoding='utf-8') as f:
            if format == 'json':
                return json.load(f)
            elif format == 'yaml':
                return yaml.safe_load(f)
            else:
                raise ValueError(f"Unsupported format: {format}")

    def load_all_from_directory(self, directory_path):
        results = []
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                _, ext = os.path.splitext(filename)
                ext = ext.lower()
                if ext in ['.json', '.yaml', '.yml']:
                    try:
                        results.append(self.load_from_file(file_path))
                    except Exception:
                        continue
        return results
