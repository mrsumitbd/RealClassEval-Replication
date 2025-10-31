
import os
import json
import yaml


class Parser:

    def load_from_file(self, file_path, format=None):
        """
        Load data from a file.

        Args:
            file_path (str): The path to the file to be loaded.
            format (str, optional): The format of the file. Defaults to None.

        Returns:
            The loaded data.

        Raises:
            ValueError: If the file format is not supported or not specified.
        """
        if format is None:
            _, file_extension = os.path.splitext(file_path)
            format = file_extension[1:]

        if format == 'json':
            with open(file_path, 'r') as file:
                return json.load(file)
        elif format == 'yaml' or format == 'yml':
            with open(file_path, 'r') as file:
                return yaml.safe_load(file)
        else:
            raise ValueError(f"Unsupported file format: {format}")

    def load_all_from_directory(self, directory_path):
        """
        Load data from all files in a directory.

        Args:
            directory_path (str): The path to the directory.

        Returns:
            A dictionary where the keys are the file names and the values are the loaded data.

        Raises:
            FileNotFoundError: If the directory does not exist.
        """
        if not os.path.exists(directory_path):
            raise FileNotFoundError(
                f"The directory '{directory_path}' does not exist.")

        data = {}
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                try:
                    data[filename] = self.load_from_file(file_path)
                except ValueError as e:
                    print(f"Skipping {filename}: {e}")
        return data
