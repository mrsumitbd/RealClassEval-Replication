class BaseTool:

    def __init__(self, tool_name=None, tool_description=None, tool_version=None, input_types=None, output_type=None, demo_commands=None, output_dir=None, user_metadata=None, model_string=None):
        self.tool_name = None
        self.tool_description = None
        self.tool_version = None
        self.input_types = None
        self.output_type = None
        self.demo_commands = None
        self.user_metadata = None
        self.output_dir = None
        self.model_string = None

        if any(v is not None for v in [tool_name, tool_description, tool_version, input_types, output_type, demo_commands, user_metadata]):
            self.set_metadata(
                tool_name=tool_name,
                tool_description=tool_description,
                tool_version=tool_version,
                input_types=input_types,
                output_type=output_type,
                demo_commands=demo_commands,
                user_metadata=user_metadata,
            )

        if output_dir is not None:
            self.set_custom_output_dir(output_dir)

        if model_string is not None:
            self.set_llm_engine(model_string)

    def set_metadata(self, tool_name, tool_description, tool_version, input_types, output_type, demo_commands, user_metadata=None):
        if tool_name is not None and not isinstance(tool_name, str):
            raise TypeError("tool_name must be a string or None")
        if tool_description is not None and not isinstance(tool_description, str):
            raise TypeError("tool_description must be a string or None")
        if tool_version is not None and not isinstance(tool_version, (str, int, float)):
            raise TypeError(
                "tool_version must be a string, int, float, or None")
        if input_types is not None and not isinstance(input_types, (list, dict, tuple, str)):
            raise TypeError(
                "input_types must be list, dict, tuple, str, or None")
        if output_type is not None and not isinstance(output_type, (str, dict, list, tuple)):
            raise TypeError(
                "output_type must be str, dict, list, tuple, or None")
        if demo_commands is not None and not isinstance(demo_commands, (list, tuple)):
            raise TypeError(
                "demo_commands must be a list or tuple of strings or None")
        if demo_commands is not None:
            for cmd in demo_commands:
                if not isinstance(cmd, str):
                    raise TypeError("Each demo command must be a string")
        if user_metadata is not None and not isinstance(user_metadata, dict):
            raise TypeError("user_metadata must be a dict or None")

        self.tool_name = tool_name
        self.tool_description = tool_description
        self.tool_version = str(
            tool_version) if tool_version is not None else None
        self.input_types = input_types
        self.output_type = output_type
        self.demo_commands = list(
            demo_commands) if demo_commands is not None else None
        self.user_metadata = dict(
            user_metadata) if user_metadata is not None else None

    def get_metadata(self):
        return {
            "tool_name": self.tool_name,
            "tool_description": self.tool_description,
            "tool_version": self.tool_version,
            "input_types": self.input_types,
            "output_type": self.output_type,
            "demo_commands": list(self.demo_commands) if self.demo_commands is not None else None,
            "user_metadata": dict(self.user_metadata) if self.user_metadata is not None else None,
            "output_dir": self.output_dir,
            "model_string": self.model_string,
        }

    def set_custom_output_dir(self, output_dir):
        '''
        Set a custom output directory for the tool.
        Parameters:
            output_dir (str): The new output directory path.
        '''
        if output_dir is None:
            self.output_dir = None
            return
        if not isinstance(output_dir, str):
            raise TypeError("output_dir must be a string or None")
        path = output_dir.strip()
        if not path:
            raise ValueError("output_dir cannot be an empty string")
        # Attempt to create the directory if it does not exist
        import os
        os.makedirs(path, exist_ok=True)
        if not os.path.isdir(path):
            raise OSError(f"Output directory path is not a directory: {path}")
        self.output_dir = path

    def set_llm_engine(self, model_string):
        if model_string is not None and not isinstance(model_string, str):
            raise TypeError("model_string must be a string or None")
        self.model_string = model_string

    def execute(self, *args, **kwargs):
        raise NotImplementedError(
            "execute() must be implemented by subclasses.")
