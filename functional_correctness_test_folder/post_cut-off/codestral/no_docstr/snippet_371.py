
class WorkflowDefinition:

    def __init__(self, name, file_path, metadata, content):

        self.name = name
        self.file_path = file_path
        self.metadata = metadata
        self.content = content

    def validate(self):

        if not isinstance(self.name, str) or not self.name:
            raise ValueError("Name must be a non-empty string")
        if not isinstance(self.file_path, str) or not self.file_path:
            raise ValueError("File path must be a non-empty string")
        if not isinstance(self.metadata, dict):
            raise ValueError("Metadata must be a dictionary")
        if not isinstance(self.content, str) or not self.content:
            raise ValueError("Content must be a non-empty string")
