class WorkflowDefinition:
    """Simple container for workflow data."""

    def __init__(self, name, file_path, metadata, content):
        """Initialize a workflow definition.

        Args:
            name (str): Name of the workflow.
            file_path (str): Path to the workflow file.
            metadata (dict): Metadata from the frontmatter.
            content (str): Content of the workflow file.
        """
        self.name = name
        self.file_path = file_path
        self.description = metadata.get('description', '')
        self.author = metadata.get('author', '')
        self.mcp_dependencies = metadata.get('mcp', [])
        self.input_parameters = metadata.get('input', [])
        self.llm_model = metadata.get('llm', None)
        self.content = content

    def validate(self):
        """Basic validation of required fields.

        Returns:
            list: List of validation errors.
        """
        errors = []
        if not self.description:
            errors.append("Missing 'description' in frontmatter")
        return errors