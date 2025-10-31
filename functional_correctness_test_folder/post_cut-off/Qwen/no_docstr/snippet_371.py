
class WorkflowDefinition:

    def __init__(self, name, file_path, metadata, content):
        self.name = name
        self.file_path = file_path
        self.metadata = metadata
        self.content = content

    def validate(self):
        if not isinstance(self.name, str) or not self.name:
            return False
        if not isinstance(self.file_path, str) or not self.file_path:
            return False
        if not isinstance(self.metadata, dict):
            return False
        if not isinstance(self.content, str) or not self.content:
            return False
        return True
