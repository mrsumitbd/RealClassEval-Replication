class BaseTool:
    '''
    A base class for building tool classes that perform specific tasks, such as image processing or text detection.
    '''

    def __init__(self, tool_name=None, tool_description=None, tool_version=None, input_types=None, output_type=None, demo_commands=None, output_dir=None, user_metadata=None, model_string=None):
        '''
        Initialize the base tool with optional metadata.
        Parameters:
            tool_name (str): The name of the tool.
            tool_description (str): A description of the tool.
            tool_version (str): The version of the tool.
            input_types (dict): The expected input types for the tool.
            output_type (str): The expected output type for the tool.
            demo_commands (list): A list of example commands for using the tool.
            output_dir (str): The directory where the tool should save its output (optional).
            user_metadata (dict): Additional metadata specific to user needs (optional).
            model_string (str): The model string for the LLM engine (optional, only used if require_llm_engine is True).
        '''
        from copy import deepcopy
        self.tool_name = None
        self.tool_description = None
        self.tool_version = None
        self.input_types = None
        self.output_type = None
        self.demo_commands = None
        self.output_dir = None
        self.user_metadata = None
        self.model_string = None

        self.set_metadata(
            tool_name=tool_name,
            tool_description=tool_description,
            tool_version=tool_version,
            input_types=input_types,
            output_type=output_type,
            demo_commands=demo_commands,
            user_metadata=deepcopy(user_metadata) if isinstance(user_metadata, dict) else (
                {} if user_metadata is None else dict(user_metadata)),
        )
        if output_dir:
            self.set_custom_output_dir(output_dir)
        if model_string:
            self.set_llm_engine(model_string)

    def set_metadata(self, tool_name, tool_description, tool_version, input_types, output_type, demo_commands, user_metadata=None):
        '''
        Set the metadata for the tool.
        Parameters:
            tool_name (str): The name of the tool.
            tool_description (str): A description of the tool.
            tool_version (str): The version of the tool.
            input_types (dict): The expected input types for the tool.
            output_type (str): The expected output type for the tool.
            demo_commands (list): A list of example commands for using the tool.
            user_metadata (dict): Additional metadata specific to user needs (optional).
        '''
        if tool_name is not None and not isinstance(tool_name, str):
            raise TypeError("tool_name must be a string or None")
        if tool_description is not None and not isinstance(tool_description, str):
            raise TypeError("tool_description must be a string or None")
        if tool_version is not None and not isinstance(tool_version, str):
            raise TypeError("tool_version must be a string or None")
        if input_types is not None and not isinstance(input_types, dict):
            raise TypeError("input_types must be a dict or None")
        if output_type is not None and not isinstance(output_type, str):
            raise TypeError("output_type must be a string or None")
        if demo_commands is not None and not isinstance(demo_commands, (list, tuple)):
            raise TypeError("demo_commands must be a list/tuple or None")
        if user_metadata is not None and not isinstance(user_metadata, dict):
            raise TypeError("user_metadata must be a dict or None")

        self.tool_name = tool_name
        self.tool_description = tool_description
        self.tool_version = tool_version
        self.input_types = input_types if input_types is not None else {}
        self.output_type = output_type
        self.demo_commands = list(
            demo_commands) if demo_commands is not None else []
        self.user_metadata = dict(
            user_metadata) if user_metadata is not None else {}
        return self

    def get_metadata(self):
        '''
        Returns the metadata for the tool.
        Returns:
            dict: A dictionary containing the tool's metadata.
        '''
        return {
            "tool_name": self.tool_name,
            "tool_description": self.tool_description,
            "tool_version": self.tool_version,
            "input_types": self.input_types,
            "output_type": self.output_type,
            "demo_commands": list(self.demo_commands) if self.demo_commands is not None else [],
            "output_dir": self.output_dir,
            "user_metadata": dict(self.user_metadata) if self.user_metadata is not None else {},
            "model_string": self.model_string,
        }

    def set_custom_output_dir(self, output_dir):
        '''
        Set a custom output directory for the tool.
        Parameters:
            output_dir (str): The new output directory path.
        '''
        if output_dir is not None and not isinstance(output_dir, str):
            raise TypeError("output_dir must be a string or None")
        self.output_dir = output_dir
        if self.output_dir:
            import os
            os.makedirs(self.output_dir, exist_ok=True)
        return self

    def set_llm_engine(self, model_string):
        '''
        Set the LLM engine for the tool.
        Parameters:
            model_string (str): The model string for the LLM engine.
        '''
        if model_string is not None and not isinstance(model_string, str):
            raise TypeError("model_string must be a string or None")
        self.model_string = model_string
        return self

    def execute(self, *args, **kwargs):
        '''
        Execute the tool's main functionality. This method should be overridden by subclasses.
        Raises:
            NotImplementedError: If the subclass does not implement this method.
        '''
        raise NotImplementedError(
            "Subclasses must implement the execute method.")
