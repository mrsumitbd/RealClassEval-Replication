
class BaseTool:
    """
    A minimal base class for tools that can be extended by specific implementations.
    """

    def __init__(
        self,
        tool_name=None,
        tool_description=None,
        tool_version=None,
        input_types=None,
        output_type=None,
        demo_commands=None,
        output_dir=None,
        user_metadata=None,
        model_string=None,
    ):
        """
        Initialize the tool with optional metadata and configuration.
        """
        self.tool_name = tool_name
        self.tool_description = tool_description
        self.tool_version = tool_version
        self.input_types = input_types or []
        self.output_type = output_type
        self.demo_commands = demo_commands or []
        self.output_dir = output_dir
        self.user_metadata = user_metadata or {}
        self.model_string = model_string

    def set_metadata(
        self,
        tool_name,
        tool_description,
        tool_version,
        input_types,
        output_type,
        demo_commands,
        user_metadata=None,
    ):
        """
        Set or update the tool's metadata.
        """
        self.tool_name = tool_name
        self.tool_description = tool_description
        self.tool_version = tool_version
        self.input_types = input_types
        self.output_type = output_type
        self.demo_commands = demo_commands
        if user_metadata is not None:
            self.user_metadata = user_metadata

    def get_metadata(self):
        """
        Return a dictionary containing the tool's metadata.
        """
        return {
            "tool_name": self.tool_name,
            "tool_description": self.tool_description,
            "tool_version": self.tool_version,
            "input_types": self.input_types,
            "output_type": self.output_type,
            "demo_commands": self.demo_commands,
            "output_dir": self.output_dir,
            "user_metadata": self.user_metadata,
            "model_string": self.model_string,
        }

    def set_custom_output_dir(self, output_dir):
        """
        Set a custom directory for the tool's output.
        """
        self.output_dir = output_dir

    def set_llm_engine(self, model_string):
        """
        Set the language‑model engine string to be used by the tool.
        """
        self.model_string = model_string

    def execute(self, *args, **kwargs):
        """
        Execute the tool's main functionality. Subclasses should override this method.
        """
        raise NotImplementedError(
            "The execute method must be implemented by subclasses.")
