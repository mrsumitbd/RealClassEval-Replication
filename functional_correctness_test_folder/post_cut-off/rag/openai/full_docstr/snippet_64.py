
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

        Parameters
        ----------
        tool_name : str, optional
            The name of the tool.
        tool_description : str, optional
            A description of the tool.
        tool_version : str, optional
            The version of the tool.
        input_types : dict, optional
            The expected input types for the tool.
        output_type : str, optional
            The expected output type for the tool.
        demo_commands : list, optional
            A list of example commands for using the tool.
        output_dir : str, optional
            The directory where the tool should save its output.
        user_metadata : dict, optional
            Additional metadata specific to user needs.
        model_string : str, optional
            The model string for the LLM engine (used only if the tool requires an LLM).
        """
        self._metadata: Dict[str, Any] = {}
        self.set_metadata(
            tool_name=tool_name,
            tool_description=tool_description,
            tool_version=tool_version,
            input_types=input_types,
            output_type=output_type,
            demo_commands=demo_commands,
            user_metadata=user_metadata,
        )
        # Output directory handling
        if output_dir is None:
            self.output_dir = Path.cwd()
        else:
            self.output_dir = Path(output_dir).expanduser().resolve()
        # LLM engine handling
        self.model_string = model_string

    # ------------------------------------------------------------------
    # Metadata handling
    # ------------------------------------------------------------------
    def set_metadata(
        self,
        tool_name: Optional[str],
        tool_description: Optional[str],
        tool_version: Optional[str],
        input_types: Optional[Dict[str, Any]],
        output_type: Optional[str],
        demo_commands: Optional[List[str]],
        user_metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Set the metadata for the tool.

        Parameters
        ----------
        tool_name : str
            The name of the tool.
        tool_description : str
            A description of the tool.
        tool_version : str
            The version of the tool.
        input_types : dict
            The expected input types for the tool.
        output_type : str
            The expected output type for the tool.
        demo_commands : list
            A list of example commands for using the tool.
        user_metadata : dict, optional
            Additional metadata specific to user needs.
        """
        self._metadata.update(
            {
                "tool_name": tool_name,
                "tool_description": tool_description,
                "tool_version": tool_version,
                "input_types": input_types,
                "output_type": output_type,
                "demo_commands": demo_commands,
                "user_metadata": user_metadata or {},
            }
        )

    def get_metadata(self) -> Dict[str, Any]:
        """
        Returns the metadata for the tool.

        Returns
        -------
        dict
            A dictionary containing the tool's metadata.
        """
        return dict(self._metadata)

    # ------------------------------------------------------------------
    # Output directory handling
    # ------------------------------------------------------------------
    def set_custom_output_dir(self, output_dir: str) -> None:
        """
        Set a custom output directory for the tool.

        Parameters
        ----------
        output_dir : str
            The new output directory path.
        """
        self.output_dir = Path(output_dir).expanduser().resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # LLM engine handling
    # ------------------------------------------------------------------
    def set_llm_engine(self, model_string: str) -> None:
        """
        Set the LLM engine for the tool.

        Parameters
        ----------
        model_string : str
            The model string for the LLM engine.
        """
        self.model_string = model_string

    # ------------------------------------------------------------------
    # Execution interface
    # ------------------------------------------------------------------
    def execute(self, *args, **kwargs):
        """
        Execute the tool's main functionality. This method should be overridden by subclasses.

        Raises
        ------
        NotImplementedError
            If the subclass does not implement this method.
        """
        raise NotImplementedError(
            f"{self.__class__.__name__}.execute() must be implemented by the subclass."
        )
