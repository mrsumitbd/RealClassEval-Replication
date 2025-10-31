
import os
import json
import yaml
import xml.etree.ElementTree as ET


class Parser:

    def load_from_file(self, file_path, format=None):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        if format is None:
            _, ext = os.path.splitext(file_path)
            format = ext.lower()[1:]  # Remove the dot

        with open(file_path, 'r') as file:
            if format == 'json':
                return json.load(file)
            elif format == 'yaml' or format == 'yml':
                return yaml.safe_load(file)
            elif format == 'xml':
                tree = ET.parse(file)
                root = tree.getroot()
                return root
            else:
                raise ValueError(f"Unsupported format: {format}")

    def load_all_from_directory(self, directory_path):
        if not os.path.isdir(directory_path):
            raise NotADirectoryError(f"Directory not found: {directory_path}")

        results = {}
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                try:
                    results[filename] = self.load_from_file(file_path)
                except ValueError:
                    continue  # Skip unsupported formats
        return results
