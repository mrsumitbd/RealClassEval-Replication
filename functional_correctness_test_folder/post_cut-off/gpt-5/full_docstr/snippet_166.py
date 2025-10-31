import argparse
import os
import re
from pathlib import Path
from typing import Any, Dict


class SearchAssistantConfig:
    '''Configuration class for the Search Assistant.'''

    _ENGINES_REQUIRING_API_KEY = {"serpapi", "brave", "tavily"}
    _KNOWN_ENGINES = {"google", "bing",
                      "duckduckgo", "serpapi", "brave", "tavily"}

    def __init__(self, args: argparse.Namespace):
        '''Initialize configuration from command line arguments.
        Args:
            args: Parsed command line arguments.
        '''
        if not isinstance(args, argparse.Namespace):
            raise TypeError("args must be an instance of argparse.Namespace")
        args_dict: Dict[str, Any] = vars(args)
        self._raw_args: Dict[str, Any] = dict(args_dict)
        for k, v in args_dict.items():
            setattr(self, k, v)

    def validate(self) -> None:
        '''Validate configuration parameters.
        Raises:
            ValueError: If any configuration parameter is invalid.
        '''
        # query
        if hasattr(self, "query"):
            if not isinstance(self.query, str) or not self.query.strip():
                raise ValueError("query must be a non-empty string")

        # engine
        if hasattr(self, "engine"):
            if not isinstance(self.engine, str) or not self.engine.strip():
                raise ValueError("engine must be a non-empty string")
            engine_norm = self.engine.strip().lower()
            if engine_norm not in self._KNOWN_ENGINES:
                raise ValueError(
                    f"engine must be one of: {sorted(self._KNOWN_ENGINES)}")
            self.engine = engine_norm  # normalize

            # api_key for engines that require it
            if engine_norm in self._ENGINES_REQUIRING_API_KEY:
                api_key = getattr(self, "api_key", None)
                if api_key is None or (isinstance(api_key, str) and not api_key.strip()):
                    raise ValueError(
                        f"api_key is required for engine '{engine_norm}'")

        # max_results
        if hasattr(self, "max_results"):
            if not isinstance(self.max_results, int) or self.max_results < 1:
                raise ValueError("max_results must be an integer >= 1")

        # timeout
        if hasattr(self, "timeout"):
            if not isinstance(self.timeout, (int, float)) or self.timeout <= 0:
                raise ValueError("timeout must be a positive number")

        # language
        if hasattr(self, "language"):
            if not isinstance(self.language, str) or not self.language.strip():
                raise ValueError("language must be a non-empty string")
            lang = self.language.strip()
            if not re.fullmatch(r"[A-Za-z]{2,3}(-[A-Za-z0-9]{2,8})*", lang):
                raise ValueError(
                    "language must be a valid IETF language tag (e.g., 'en', 'en-US')")
            self.language = lang

        # output_file
        if hasattr(self, "output_file") and self.output_file is not None:
            if not isinstance(self.output_file, (str, os.PathLike)):
                raise ValueError("output_file must be a path-like value")
            out_path = Path(self.output_file)
            parent = out_path.parent if out_path.suffix else out_path
            if parent and str(parent) not in ("", ".") and not parent.exists():
                raise ValueError(
                    f"Directory does not exist for output_file: {parent}")

        # cache_dir
        if hasattr(self, "cache_dir") and self.cache_dir is not None:
            if not isinstance(self.cache_dir, (str, os.PathLike)):
                raise ValueError("cache_dir must be a path-like value")
            cache_path = Path(self.cache_dir)
            if cache_path.exists() and not cache_path.is_dir():
                raise ValueError("cache_dir exists but is not a directory")

        # verbose
        if hasattr(self, "verbose"):
            if not isinstance(self.verbose, bool):
                raise ValueError("verbose must be a boolean")

        # retries
        if hasattr(self, "retries"):
            if not isinstance(self.retries, int) or self.retries < 0:
                raise ValueError("retries must be a non-negative integer")
