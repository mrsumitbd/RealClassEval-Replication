from pathlib import Path
from copy import deepcopy


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
        # Subclasses may override this flag
        if not hasattr(self, 'require_llm_engine'):
            self.require_llm_engine = False

        # Initialize metadata container
        self._metadata = {}
        self.set_metadata(
            tool_name=tool_name or self.__class__.__name__,
            tool_description=tool_description or '',
            tool_version=tool_version or '0.0.0',
            input_types=input_types or {},
            output_type=output_type or '',
            demo_commands=demo_commands or [],
            user_metadata=user_metadata or {}
        )

        # Output directory handling
        if output_dir is None:
            default_dir = Path.cwd() / 'tool_outputs' / \
                (self._metadata.get('tool_name') or self.__class__.__name__)
            default_dir.mkdir(parents=True, exist_ok=True)
            self.output_dir = str(default_dir)
        else:
            self.set_custom_output_dir(output_dir)

        # LLM engine configuration (optional)
        self.model_string = None
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
        self._metadata = {
            'tool_name': tool_name,
            'tool_description': tool_description,
            'tool_version': tool_version,
            'input_types': dict(input_types or {}),
            'output_type': output_type,
            'demo_commands': list(demo_commands or []),
            'user_metadata': dict(user_metadata or {}),
        }

    def get_metadata(self):
        '''
        Returns the metadata for the tool.
        Returns:
            dict: A dictionary containing the tool's metadata.
        '''
        # Include runtime attributes that may be useful for introspection
        meta = deepcopy(self._metadata)
        meta['output_dir'] = getattr(self, 'output_dir', None)
        if getattr(self, 'require_llm_engine', False):
            meta['model_string'] = getattr(self, 'model_string', None)
        return meta

    def set_custom_output_dir(self, output_dir):
        '''
        Set a custom output directory for the tool.
        Parameters:
            output_dir (str): The new output directory path.
        '''
        path = Path(output_dir).expanduser().resolve()
        path.mkdir(parents=True, exist_ok=True)
        self.output_dir = str(path)

    def set_llm_engine(self, model_string):
        '''
        Set the LLM engine for the tool.
        Parameters:
            model_string (str): The model string for the LLM engine.
        '''
        self.model_string = model_string

    def execute(self, *args, **kwargs):
        '''
        Execute the tool's main functionality. This method should be overridden by subclasses.
        Raises:
            NotImplementedError: If the subclass does not implement this method.
        '''
        raise NotImplementedError(
            'Subclasses must implement the execute method.')
