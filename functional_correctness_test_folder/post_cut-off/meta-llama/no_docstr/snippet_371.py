
import json
import os


class WorkflowDefinition:

    def __init__(self, name, file_path, metadata, content):
        self.name = name
        self.file_path = file_path
        self.metadata = metadata
        self.content = content

    def validate(self):
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Name must be a non-empty string")

        if not isinstance(self.file_path, str) or not self.file_path.strip():
            raise ValueError("File path must be a non-empty string")

        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File {self.file_path} does not exist")

        if not isinstance(self.metadata, dict):
            raise ValueError("Metadata must be a dictionary")

        try:
            json.loads(self.content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON content: {e}")
