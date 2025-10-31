
import logging
import os
from typing import Optional


class Config:
    """
    Configuration holder for the application.

    Parameters
    ----------
    logger : logging.Logger
        Logger instance to use.
    mcp_port : int, default 8765
        Port for the MCP server.
    model : str, default 'gemini/gemini-2.5-flash'
        Model identifier.
    output_dir : str, default ''
        Directory where output files will be written. If empty, defaults to
        ``{project_path}/output``.
    temperature : float, default 0
        Sampling temperature for the model.
    max_iterations : int, default 50
        Maximum number of iterations for the model loop.
    host : str, default 'localhost'
        Host address for the MCP server.
    prompt : str | None, default None
        Optional prompt to prepend to every request.
    confidence : int, default 7
        Confidence threshold for the model.
    project_path : str, default ''
        Base path of the project. Used to construct default output directory.
    """

    def __init__(
        self,
        logger: logging.Logger,
        mcp_port: int = 8765,
        model: str = "gemini/gemini-2.5-flash",
        output_dir: str = "",
        temperature: float = 0,
        max_iterations: int = 50,
        host: str = "localhost",
        prompt: Optional[str] = None,
        confidence: int = 7,
        project_path: str = "",
    ):
        self.logger = logger
        self.mcp_port = mcp_port
        self.model = model
        self.temperature = temperature
        self.max_iterations = max_iterations
        self.host = host
        self.prompt = prompt
        self.confidence = confidence
        self.project_path = project_path

        # Resolve output directory
        if output_dir:
            self.output_dir = output_dir
        else:
            self.output_dir = os.path.join(project_path, "output")

        # Determine provider and API key
        self.provider = self._get_provider_from_model(model)
        self.api_key = self._get_api_key_for_model(model)

        # Log basic configuration
        self.logger.debug(
            f"Config initialized: provider={self.provider}, "
            f"api_key={'set' if self.api_key else 'not set'}, "
            f"output_dir={self.output_dir}"
        )

    # --------------------------------------------------------------------- #
    # Helper methods
    # --------------------------------------------------------------------- #

    def _get_provider_from_model(self, model: str) -> str:
        """
        Extract the provider name from a model identifier.

        Parameters
        ----------
        model : str
            Model identifier, e.g. 'gemini/gemini-2.5-flash'.

        Returns
        -------
        str
            Provider name, e.g. 'gemini'.
        """
        if "/" in model:
            return model.split("/", 1)[0].lower()
        # If no slash, assume the whole string is the provider
        return model.lower()

    def _get_env_var_for_provider(self, provider: str) -> str:
        """
        Map a provider name to the expected environment variable name.

        Parameters
        ----------
        provider : str
            Provider name, e.g. 'gemini'.

        Returns
        -------
        str
            Environment variable name that should contain the API key.
        """
        mapping = {
            "gemini": "GEMINI_API_KEY",
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
            "cohere": "COHERE_API_KEY",
            "google": "GOOGLE_API_KEY",
            "mistral": "MISTRAL_API_KEY",
            "huggingface": "HUGGINGFACE_API_KEY",
        }
        return mapping.get(provider.lower(), f"{provider.upper()}_API_KEY")

    def _get_api_key_for_model(self, model_name: str) -> Optional[str]:
        """
        Retrieve the API key for a given model from environment variables.

        Parameters
        ----------
        model_name : str
            Full model identifier.

        Returns
        -------
        str | None
            The API key if found, otherwise None.
        """
        provider = self._get_provider_from_model(model_name)
        env_var = self._get_env_var_for_provider(provider)
        key = os.getenv(env_var)
        if key:
            self.logger.debug(
                f"Found API key for provider '{provider}' in env var '{env_var}'.")
        else:
            self.logger.warning(
                f"API key for provider '{provider}' not found in env var '{env_var}'."
            )
        return key
