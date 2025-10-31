
import os
import json
from pathlib import Path


class BaseTool:
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
        self._metadata = {}
        self.set_metadata(
            tool_name,
            tool_description,
            tool_version,
            input_types,
            output_type,
            demo_commands,
            user_metadata,
        )
        self._output_dir = Path(output_dir) if output_dir else Path.cwd()
        self._output_dir.mkdir(parents=True, exist_ok=True)
        self._model_string = model_string

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
        self._metadata = {
            "tool_name": tool_name,
            "tool_description": tool_description,
            "tool_version": tool_version,
            "input_types": input_types,
            "output_type": output_type,
            "demo_commands": demo_commands,
            "user_metadata": user_metadata or {},
        }

    def get_metadata(self):
        return self._metadata.copy()

    def set_custom_output_dir(self, output_dir):
        """
        Set a custom output directory for the tool.
        Parameters:
            output_dir (str): The new output directory path.
        """
        self._output_dir = Path(output_dir)
        self._output_dir.mkdir(parents=True, exist_ok=True)

    def set_llm_engine(self, model_string):
        self._model_string = model_string

    def execute(self, *args, **kwargs):
        """
        Execute the tool with the provided arguments.
        Subclasses should override this method.
        """
        raise NotImplementedError(
            "Subclasses must implement the execute method.")
