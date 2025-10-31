
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
                return self._xml_to_dict(root)
            else:
                raise ValueError(f"Unsupported file format: {format}")

    def _xml_to_dict(self, element):
        result = {}
        for child in element:
            if len(child) > 0:
                value = self._xml_to_dict(child)
            else:
                value = child.text
            if child.tag in result:
                if isinstance(result[child.tag], list):
                    result[child.tag].append(value)
                else:
                    result[child.tag] = [result[child.tag], value]
            else:
                result[child.tag] = value
        return result

    def load_all_from_directory(self, directory_path):
        '''Return a list of dict from a directory containing files
        '''
        if not os.path.isdir(directory_path):
            raise NotADirectoryError(f"Directory not found: {directory_path}")

        results = []
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                try:
                    data = self.load_from_file(file_path)
                    results.append(data)
                except ValueError as e:
                    print(f"Skipping file {filename}: {e}")
        return results
