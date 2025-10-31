
class WorkflowDefinition:

    def __init__(self, name, file_path, metadata, content):
        self.name = name
        self.file_path = file_path
        self.metadata = metadata
        self.content = content

    def validate(self):
        errors = []
        if not self.name:
            errors.append("Name is required.")
        if not self.file_path:
            errors.append("File path is required.")
        if not self.metadata:
            errors.append("Metadata is required.")
        if not self.content:
            errors.append("Content is required.")
        return errors
