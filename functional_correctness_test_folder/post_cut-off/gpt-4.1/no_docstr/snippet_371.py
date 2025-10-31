
class WorkflowDefinition:

    def __init__(self, name, file_path, metadata, content):
        self.name = name
        self.file_path = file_path
        self.metadata = metadata
        self.content = content

    def validate(self):
        if not isinstance(self.name, str) or not self.name.strip():
            return False
        if not isinstance(self.file_path, str) or not self.file_path.strip():
            return False
        if not isinstance(self.metadata, dict):
            return False
        if self.content is None or (isinstance(self.content, str) and not self.content.strip()):
            return False
        return True
