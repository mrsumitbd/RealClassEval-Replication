
import os
from pathlib import Path
from typing import Any, Dict, List, Optional


class BaseTool:
    """
    A base class for building tool classes that perform specific tasks,
    such as image processing or text detection.
    """

    def __init__(
        self,
        tool_name: Optional[str] = None,
        tool_description: Optional[str] = None,
        tool_version: Optional[str] = None,
        input_types: Optional[Dict[str, Any]] = None,
        output_type: Optional[str] = None,
        demo_commands: Optional[List[str]] = None,
        output_dir: Optional[str] = None,
        user_metadata: Optional[Dict[str, Any]] = None,
        model_string: Optional[str] = None,
    ):
        """
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
            model_string (str): The model string for the LLM engine (optional, only used if
                                require_llm_engine is True).
        """
        self.metadata: Dict[str, Any] = {}
        if tool_name or tool_description or tool_version or input_types or output_type or demo_commands:
            self.set_metadata(
                tool_name=tool_name,
                tool_description=tool_description,
                tool_version=tool_version,
                input_types=input_types,
                output_type=output_type,
                demo_commands=demo_commands,
                user_metadata=user_metadata,
            )
        else:
            # Default empty metadata
            self.metadata = {
                "tool_name": None,
                "tool_description": None,
                "tool_version": None,
                "input_types": {},
                "output_type": None,
                "demo_commands": [],
                "user_metadata": {},
            }

        # Output directory handling
        if output_dir:
            self.set_custom_output_dir(output_dir)
        else:
            self.output_dir = Path.cwd()

        # LLM engine handling
        self.model_string = model_string

    def set_metadata(
        self,
        tool_name: str,
        tool_description: str,
        tool_version: str,
        input_types: Dict[str, Any],
        output_type: str,
        demo_commands: List[str],
        user_metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Set the metadata for the tool.

        Parameters:
            tool_name (str): The name of the tool.
            tool_description (str): A description of the tool.
            tool_version (str): The version of the tool.
            input_types (dict): The expected input types for the tool.
            output_type (str): The expected output type for the tool.
            demo_commands (list): A list of example commands for using the tool.
            user_metadata (dict): Additional metadata specific to user needs (optional).
        """
        self.metadata = {
            "tool_name": tool_name,
            "tool_description": tool_description,
            "tool_version": tool_version,
            "input_types": input_types or {},
            "output_type": output_type,
            "demo_commands": demo_commands or [],
            "user_metadata": user_metadata or {},
        }

    def get_metadata(self) -> Dict[str, Any]:
        """
        Returns the metadata for the tool.

        Returns:
            dict: A dictionary containing the tool's metadata.
        """
        return self.metadata

    def set_custom_output_dir(self, output_dir: str):
        """
        Set a custom output directory for the tool.

        Parameters:
            output_dir (str): The new output directory path.
        """
        path = Path(output_dir).expanduser().resolve()
        path.mkdir(parents=True, exist_ok=True)
        self.output_dir = path

    def set_llm_engine(self, model_string: str):
        """
        Set the LLM engine for the tool.

        Parameters:
            model_string (str): The model string for the LLM engine.
        """
        self.model_string = model_string

    def execute(self, *args, **kwargs):
        """
        Execute the tool's main functionality. This method should be overridden by subclasses.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        raise NotImplementedError(
            "Subclasses must implement the execute method.")
