
class BaseTool:

    def __init__(self, tool_name=None, tool_description=None, tool_version=None, input_types=None, output_type=None, demo_commands=None, output_dir=None, user_metadata=None, model_string=None):
        self.tool_name = tool_name
        self.tool_description = tool_description
        self.tool_version = tool_version
        self.input_types = input_types
        self.output_type = output_type
        self.demo_commands = demo_commands
        self.output_dir = output_dir
        self.user_metadata = user_metadata if user_metadata is not None else {}
        self.model_string = model_string

    def set_metadata(self, tool_name, tool_description, tool_version, input_types, output_type, demo_commands, user_metadata=None):
        self.tool_name = tool_name
        self.tool_description = tool_description
        self.tool_version = tool_version
        self.input_types = input_types
        self.output_type = output_type
        self.demo_commands = demo_commands
        if user_metadata is not None:
            self.user_metadata = user_metadata

    def get_metadata(self):
        return {
            'tool_name': self.tool_name,
            'tool_description': self.tool_description,
            'tool_version': self.tool_version,
            'input_types': self.input_types,
            'output_type': self.output_type,
            'demo_commands': self.demo_commands,
            'user_metadata': self.user_metadata
        }

    def set_custom_output_dir(self, output_dir):
        self.output_dir = output_dir

    def set_llm_engine(self, model_string):
        self.model_string = model_string

    def execute(self, *args, **kwargs):
        raise NotImplementedError(
            "The execute method must be implemented by the subclass.")
