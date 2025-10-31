import os
import copy
from datetime import datetime


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
        self.require_llm_engine = False
        self._metadata = {}
        self.output_dir = None
        self.model_string = None

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
        if input_types is not None and not isinstance(input_types, dict):
            raise TypeError('input_types must be a dict or None')
        if demo_commands is not None and not isinstance(demo_commands, (list, tuple)):
            raise TypeError('demo_commands must be a list, tuple, or None')
        if user_metadata is not None and not isinstance(user_metadata, dict):
            raise TypeError('user_metadata must be a dict or None')

        now = datetime.utcnow().isoformat() + 'Z'
        created_at = self._metadata.get('created_at', now)

        self._metadata = {
            'tool_name': tool_name,
            'tool_description': tool_description,
            'tool_version': tool_version,
            'input_types': input_types or {},
            'output_type': output_type,
            'demo_commands': list(demo_commands) if demo_commands is not None else [],
            'user_metadata': user_metadata or {},
            'output_dir': self.output_dir,
            'require_llm_engine': bool(getattr(self, 'require_llm_engine', False)),
            'model_string': self.model_string,
            'created_at': created_at,
            'updated_at': now,
        }

    def get_metadata(self):
        '''
        Returns the metadata for the tool.
        Returns:
            dict: A dictionary containing the tool's metadata.
        '''
        return copy.deepcopy(self._metadata)

    def set_custom_output_dir(self, output_dir):
        '''
        Set a custom output directory for the tool.
        Parameters:
            output_dir (str): The new output directory path.
        '''
        if output_dir is None:
            self.output_dir = None
        else:
            if not isinstance(output_dir, str):
                raise TypeError('output_dir must be a string or None')
            path = os.path.abspath(os.path.expanduser(output_dir))
            os.makedirs(path, exist_ok=True)
            self.output_dir = path

        # Reflect change in metadata
        if self._metadata:
            self._metadata['output_dir'] = self.output_dir
            self._metadata['updated_at'] = datetime.utcnow().isoformat() + 'Z'

    def set_llm_engine(self, model_string):
        '''
        Set the LLM engine for the tool.
        Parameters:
            model_string (str): The model string for the LLM engine.
        '''
        if model_string is not None and not isinstance(model_string, str):
            raise TypeError('model_string must be a string or None')
        self.model_string = model_string
        if self._metadata:
            self._metadata['model_string'] = self.model_string
            self._metadata['updated_at'] = datetime.utcnow().isoformat() + 'Z'

    def execute(self, *args, **kwargs):
        '''
        Execute the tool's main functionality. This method should be overridden by subclasses.
        Raises:
            NotImplementedError: If the subclass does not implement this method.
        '''
        raise NotImplementedError(
            'Subclasses must implement the execute method.')
